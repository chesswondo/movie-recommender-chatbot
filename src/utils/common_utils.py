import torch
import json

def extract_between(text: str, start: str, end: str) -> str:
    # Find the start and end positions
    start_idx = text.find(start) + len(start)
    end_idx = text.find(end, start_idx)
    
    # Extract the substring if both start and end are found
    if start_idx != -1 and end_idx != -1:
        return text[start_idx:end_idx]
    else:
        return text
    
def set_device(device: str) -> str:
    if torch.cuda.is_available():
        return device
    return "cpu"

def load_config(config_path: str) -> dict:
    """
    Loads config file.

    : param config_path: (str) - path to config file.
    
    : return: (dict) - config dict.
    """
    with open(config_path, "r") as f:
        return json.load(f)