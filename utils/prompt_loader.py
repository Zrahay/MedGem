from pathlib import Path

def load_prompt(path):
    return Path(path).read_text()
