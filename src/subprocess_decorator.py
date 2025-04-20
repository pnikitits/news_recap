import multiprocessing
import traceback
import time
import functools
import cloudpickle



def _process_func(queue, pickled_func):
    """
    Function that will run in the subprocess. Uses cloudpickle to unpickle
    the function and its closure.
    """
    try:
        # Unpickle the function
        func = cloudpickle.loads(pickled_func)
        # Run the function
        result = func()
        queue.put(('success', result))
    except Exception as e:
        queue.put(('error', traceback.format_exc()))
    finally:
        queue.put(('done', None))

def run_in_subprocess(func):
    """
    A decorator to run the function in a subprocess to ensure
    GPU memory is freed after the process completes.
    Uses cloudpickle to handle pickling of closures and nested functions.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a new function that includes the args and kwargs
        def pickled_target():
            return func(*args, **kwargs)
        
        # Pickle the entire function with its closure
        pickled_func = cloudpickle.dumps(pickled_target)
        
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=_process_func, args=(queue, pickled_func))
        process.start()
        
        result = None
        error = None
        process_finished = False
        
        while True:
            if not process.is_alive():
                process_finished = True
                
            try:
                status, data = queue.get(block=False)
                if status == 'success':
                    result = data
                elif status == 'error':
                    error = data
                elif status == 'done':
                    process_finished = True
            except multiprocessing.queues.Empty:
                pass
                
            if process_finished and (result is not None or error is not None):
                break
                
            time.sleep(0.1)
            
        if process.is_alive():
            process.terminate()
            
        process.join()
        
        if error:
            raise Exception(f"Error in subprocess:\n{error}")
        elif result is None:
            raise Exception("Subprocess completed without returning a result")
            
        return result
    
    return wrapper

