# News Recap


A Python project that:
- Scrapes **news headlines** (e.g. from BBC News)
- Uses a **local LLM** (e.g. Meta-Llama 3.1 8B) to classify each headline as _"ok news"_ or _"depressing news"_
- Generates a clean **PDF report** with separate sections for each type of news
- Automates hourly reports via **cron**



## Features

- **Headline classification** using a local quantized LLM (`gguf`) for offline use
- **PDF generation**:
    - "Ok News" section: standard formatting
    - "Depressing News" section: lower visual weight with **alpha set to 0.4** for subtle display
- **Cron support**: run every hour with an included shell script



## Project Structure

```
├── main.py                  # Main script to run the full pipeline
├── src/
│   ├── news.py              # News headline scraper
│   ├── local_gguf.py        # LLM interface
│   └── make_pdf.py          # PDF report generator
├── run_main_script.sh       # Script to run main.py
├── setup_cron.sh            # Cron job installer
├── install_dependencies.sh  # Install dependencies (this has the Metal version of llama-cpp-python)
├── config.yaml              # Configs for scraper, model path, output etc.
├── requirements.txt         # Python package dependencies
├── models/                  # LLM model files (gguf)
├── doc/
│   ├── sample.pdf           # Sample output
│   └── auto_news_log.log    # Logging
└── venv/                    # Python virtual environment
```



## Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/pnikitits/news_recap.git
```

### 2. Install dependencies
```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### 3. Run manually
```bash
chmod +x run_main_script.sh
./run_main_script.sh
```

### 4. Set up cron to run hourly
```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

### macOS Permissions Note

Due to macOS sandboxing and permission restrictions:

**This project should be located in your `/Users/yourname/` folder and not in `/Documents`, `/Desktop`, or `/Downloads`.**

Placing it inside a protected folder may cause permission errors when running cron jobs or scripts.


## Model Info

This project uses [Meta-Llama 3.1 8B Instruct Q8_0](https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF) in GGUF format for local inference. Make sure you have enough memory (8GB) and install `llama-cpp-python` with GPU or CPU support depending on your setup.



## Configuration

Edit `config.yaml` to customize:
- Output path
- Model path
- News source URL
