from llama_cpp import Llama



def format_chat_prompt(messages):
    """
    Format a list of messages into the Llama 3.1 chat format.
    
    Each message should be a dict with 'role' and 'content' keys.
    Roles can be: 'system', 'user', 'assistant'
    
    Returns formatted prompt string ready for the model.
    """
    formatted_messages = []
    
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        
        if role == "system":
            formatted_messages.append(f"<|system|>\n{content}")
        elif role == "user":
            formatted_messages.append(f"<|user|>\n{content}")
        elif role == "assistant":
            formatted_messages.append(f"<|assistant|>\n{content}")
        else:
            raise ValueError(f"Unknown role: {role}")
    
    formatted_messages.append("<|assistant|>")
    
    return "\n".join(formatted_messages)
    
    
class Model:
    def __init__(self, model_path):
        self.model = Llama(
            model_path=model_path,
            n_ctx=1024,
            n_gpu_layers=-1,
            use_mlock=True,
            verbose=False,
        )
        
    def run(self, system_prompt=None, user_prompt=None, conversation=None, remember_conversation=False):
        """
        Run Llama model with properly formatted chat prompt.
        
        Args:
            system_prompt: String containing system prompt
            user_prompt: String containing user prompt
            conversation: List of message dicts with 'role' and 'content' keys
                         (overrides system_prompt and user_prompt if provided)
            remember_conversation: Boolean to remember conversation context
        
        Returns:
            Generated text from the model
        """
        if conversation is None:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            if user_prompt:
                messages.append({"role": "user", "content": user_prompt})
        else:
            messages = conversation
        
        formatted_prompt = format_chat_prompt(messages)
        
        output = self.model(
            formatted_prompt,
            max_tokens=128,
            temperature=0.7,
            stop=["<|user|>", "<|system|>"]
        )
        
        generated_text = output["choices"][0]["text"]
        for token in ["|</assistant|>", "</|user|>", "</assistant>", "<|user|>", "<|assistant|>", "|"]:
            generated_text = generated_text.replace(token, "").strip()
        
        
        if remember_conversation:
            messages.append({"role": "assistant", "content": generated_text})
        
        return generated_text
        
