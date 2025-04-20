from src.news import analyze_and_fetch_bbc_headlines
from src.local_gguf import Model
from src.make_pdf import sort_lines, generate_pdf
import sys
from pathlib import Path
import logging
import yaml



if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent

CONFIG_PATH = BASE_DIR / "config.yaml"

try:
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    logging.error(f"Configuration file not found: {CONFIG_PATH}")
    sys.exit(1)
except yaml.YAMLError as e:
    logging.error(f"Error parsing YAML configuration file: {e}")
    sys.exit(1)
    
    

OUTPUT_PATH = config.get("files", {}).get("output_pdf", str(BASE_DIR / "sample_output.pdf"))
LOG_FILENAME = config.get("files", {}).get("log_file", str(BASE_DIR / "auto_news_log.log"))
LOGGING_LEVEL = getattr(logging, config.get("logging", {}).get("level", "INFO").upper())
LOGGING_FORMAT = config.get("logging", {}).get("format", "%(asctime)s - %(levelname)s - %(message)s")
LLM_PATH = config.get("files", {}).get("llm_path", str(BASE_DIR / "Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"))
NEWS_WEB_URL = config.get("content", {}).get("news_source", "https://www.bbc.com/news")
NEWS_N_ARTICLES = config.get("content", {}).get("n_articles", 15)    

    
logging.basicConfig(
    filename=LOG_FILENAME,
    level=LOGGING_LEVEL,
    format=LOGGING_FORMAT,
)
    



def red(text: str) -> str:
    return f"\033[91m{str(text)}\033[0m"
def green(text: str) -> str:
    return f"\033[92m{str(text)}\033[0m"




if __name__ == "__main__":
    model = Model(LLM_PATH)
    
    headlines = analyze_and_fetch_bbc_headlines()
    headlines = [h.get_text().strip() for h in headlines]
    
    responses = []
    
    for headline in headlines:
        
        system = "System prompt: You are a news headline analyzer. You will be given a news headline and need to say if it is depressing or not. ONLY return 'depressing news' or 'ok news'."
        user = f"User prompt: {headline}"
        
        
        
        response = model.run(system_prompt=system, user_prompt=user).strip().lower()
        if "depressing" in response:
            response = red(response)
            responses.append("depressing")
        else:
            response = green(response)
            responses.append("ok")
        print(f"[{response}] {headline}")
        
        
    
    positive_headlines, negative_headlines = sort_lines(headlines, responses)
    pdf_path = generate_pdf(
        positive_headlines=positive_headlines,
        negative_headlines=negative_headlines,
        output_path=OUTPUT_PATH,
    )
