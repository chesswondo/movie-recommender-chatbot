from transformers.agents.llm_engine import MessageRole, get_clean_message_list
from transformers.agents.llm_engine import HfApiEngine
from typing import Any

role_conversions = {
    MessageRole.TOOL_RESPONSE: MessageRole.USER,
}

class CustomLLM:
    """Class for working with LLMs using Hugging Face API."""
    
    def __init__(self,
                 model_name: str) -> None:
        """
        Initializes an instance of CustomLLM.

        : param model_name: (str) - name of the language model.

        : return: (None) - this function does not return any value.
        """        
        self._hf_api_engine = HfApiEngine(model=model_name)

    def __call__(self,
                 messages: Any,
                 stop_sequences: list = [],
                 **kwargs) -> str:
        """
        Call function for CustomLLM.

        : param messages: (Any) - input messages.
        : param stop_sequences: (list) - list of stop sequences for generation.
        
        : return: (str) - processed model response.
        """
        if type(messages) is not str:
            messages = get_clean_message_list(message_list=messages, role_conversions=role_conversions)
        
        else:
            messages = [{"role": "user", "content": messages}]
        
        # Use HfApiEngine to handle the request
        return self._hf_api_engine(messages, stop_sequences=stop_sequences, **kwargs)

