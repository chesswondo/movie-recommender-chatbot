import torch
import json
    
def set_device(device: str) -> str:
    """
    Sets device type based on given input and system parameters.

    : param device: (str) - input device value.
    
    : return: (str) - final device type (cpu or cuda).
    """
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