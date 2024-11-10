from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from typing import Any
import os

class CustomLLM:
    def __init__(self,
                 model_name: str,
                 cache_dir: str,
                 max_new_tokens: int,
                 device: str,
                 task: str,
                 allow_download: bool=False) -> None:
        
        # Check folder path
        if not allow_download and not os.path.exists(cache_dir):
            print(os.path.abspath(cache_dir))
            raise ValueError("Folder with model weights doesn't exist. \
                             Check specified folder path or change allow_download argument to True")
        
        # Specify the local folder for the model weights and device for the model to run on
        self._cache_dir = cache_dir
        self._device = device

        # Use specified model and define the local cache directory
        self._tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, token=True)
        self._model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir, token=True).to(device)

        # Create a text generation pipeline
        self._pipe = pipeline(task, model=self._model, tokenizer=self._tokenizer, max_new_tokens=max_new_tokens, device=device)
        self._hf = HuggingFacePipeline(pipeline=self._pipe)

    def __call__(self,
                 messages: Any) -> str:
        
        return self._hf.invoke(messages)