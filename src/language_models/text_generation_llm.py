from transformers.agents.llm_engine import MessageRole
from transformers.agents.llm_engine import HfApiEngine
from typing import Any

from utils.llm_utils import extract_text, extract_role_pairs
from utils.telegram_utils import SpecialSymbol

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
        message_type = type(messages)
        if message_type is not list:
            if message_type is str:
                messages = [{"role": MessageRole.USER, "content": messages}]
            else:
                raise TypeError(f"Input messages must be either list or str, however got {message_type}.")
        
        else:
            # Retrieve context during first call
            if len(messages) == 2 and messages[0]['role'] == MessageRole.SYSTEM:
                context, current_message = extract_text(messages[-1]['content'], SpecialSymbol.START_CONTEXT.value, SpecialSymbol.END_CONTEXT.value)
                messages = messages[:-1]
                for msg in extract_role_pairs(input_string=context, role1=SpecialSymbol.USER.value, role2=SpecialSymbol.BOT.value):
                    role = MessageRole.USER if msg[0] == SpecialSymbol.USER.value else MessageRole.ASSISTANT
                    messages.append({'role': role, 'content': msg[1]})
                messages.append({'role': MessageRole.USER, 'content': current_message})

        # Use HfApiEngine to handle the request
        return self._hf_api_engine(messages, stop_sequences=stop_sequences, **kwargs)

