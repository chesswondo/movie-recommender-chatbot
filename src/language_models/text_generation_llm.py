from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from typing import Any
import os

class CustomLLM:
    """Class for working with LLMs from Hugging Face."""
    
    def __init__(self,
                 model_name: str,
                 cache_dir: str,
                 max_new_tokens: int,
                 task: str,
                 allow_download: bool,
                 load_in_8bit: bool) -> None:
        """
        Initializes an instance of CustomLLM.

        : param model_name: (str) - name of the language model.
        : param cache_dir: (str) - path to the directory where to store model weights.
        : param max_new_tokens: (int) - max number of tokens to generate.
        : param task: (str) - task for the model (like 'text-generation').
        : param allow_download: (bool) - whether to download model weights if they are not available locally.
        : param load_in_8bit: (bool) - whether to apply 8-bit quantization for saving resources.

        : return: (None) - this function does not return any value.
        """
        
        # Check folder path
        if not allow_download and not os.path.exists(cache_dir):
            print(os.path.abspath(cache_dir))
            raise ValueError("Folder with model weights doesn't exist. \
                             Check specified folder path or change allow_download argument to True")
        
        # Use specified model and define the local cache directory
        self._tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, token=True)
        self._model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir, token=True, device_map="auto", load_in_8bit=load_in_8bit)

        # Create a text generation pipeline
        self._pipe = pipeline(task, model=self._model, tokenizer=self._tokenizer, max_new_tokens=max_new_tokens)
        self._hf = HuggingFacePipeline(pipeline=self._pipe)

    def __call__(self,
                 messages: Any) -> str:
        """Call function for CustomLLM.

        : param messages: (Any) - input messages.
        
        : return: (str) - model response.
        """
        
        return self._hf.invoke(messages)