# ClaudePromptProcessor.py

from typing import List, Union, Optional
from AbstractPromptProcessor import AbstractPromptProcessor

try:
    import anthropic
except ImportError:
    anthropic = None

class ClaudePromptProcessor(AbstractPromptProcessor):
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-haiku-20240307"):
        super().__init__(api_key)
        self.model = model
        
    def generate_response(
        self,
        prompt: Union[str, List[str]],
        *,
        model: Optional[str] = "claude-3-haiku-20240307",
        max_tokens: Optional[int] = 4096,
        temperature: float = 1.0,
        top_p: float = 1.0,
        logprobs: Optional[int] = None,
        stream: bool = False,
        system: Optional[str] = None,
        # Claude specific arguments
        metadata: Optional[dict] = None,
        stop_sequences: Optional[List[str]] = None,
        tool_choice: Optional[Union[str, dict]] = None,
        tools: Optional[List[dict]] = None,
        top_k: Optional[int] = None,
        user: Optional[str] = None,
    ) -> Union[str, List[str]]:
        if anthropic is None:
            raise ImportError("The 'anthropic' library is not installed. Please install it to use ClaudePromptProcessor.")
        if model is None:
            model = self.model
        
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stop_sequences": stop_sequences,
            "logprobs": logprobs,
            "metadata": metadata,
            "system": super().remove_special_characters(system),
            "tool_choice": tool_choice,
            "tools": tools,
            "top_k": top_k,
            "user_id": user,
        }
        
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        
        messages = []
        if isinstance(prompt, str):
            messages.append({"role": "user", "content": super().remove_special_characters(prompt)})
        else:
            messages.extend([{"role": "user", "content": super().remove_special_characters(p)} for p in prompt])

        response = anthropic.Anthropic().messages.create(messages=messages, **kwargs) if stream else anthropic.Anthropic().messages.create(messages=messages, **kwargs)
        
        return response.content[0].text