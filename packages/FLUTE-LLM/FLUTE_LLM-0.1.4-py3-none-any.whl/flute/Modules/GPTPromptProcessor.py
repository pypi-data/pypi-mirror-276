# GPTPromptProcessor.py

from typing import List, Union, Optional
import flute
from flute.Modules.AbstractPromptProcessor import AbstractPromptProcessor

try:
    import openai
except ImportError:
    openai = None

class GPTPromptProcessor(AbstractPromptProcessor):
    def __init__(self, api_key: Optional[str] = None, organization: Optional[str] = None, model: str = "gpt-4o"):
        super().__init__(api_key)
        self.organization = organization

    def generate_response(
        self,
        prompt: Union[str, List[str]],
        *,
        model: str = "gpt-4o",
        max_tokens: Optional[int] = 4096,
        temperature: float = 1.0,
        top_p: float = 1.0,
        n: int = 1,
        stop: Optional[Union[str, List[str]]] = None,
        logprobs: Optional[int] = None,
        stream: bool = False,
        system: Optional[str] = None,
        # GPT specific arguments
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        logit_bias: Optional[dict] = None,
        top_logprobs: Optional[int] = None,
        response_format: Optional[dict] = None,
        seed: Optional[int] = None,
        stream_options: Optional[dict] = None,
        tools: Optional[List[dict]] = None,
        tool_choice: Optional[Union[str, dict]] = None,
        user: Optional[str] = None,
    ) -> Union[str, List[str]]:
        if openai is None:
            raise ImportError("The 'openai' library is not installed. Please install it to use GPTPromptProcessor.")
        openai.api_key = self.api_key
        if self.organization:
            openai.organization = self.organization

        messages = []
        if system is not None:
            messages.append({"role": "system", "content": super().remove_special_characters(system)})
        if isinstance(prompt, str):
            messages.append({"role": "user", "content": super().remove_special_characters(prompt)})
        else:
            messages.extend([{"role": "user", "content": super().remove_special_characters(p)} for p in prompt])

        kwargs = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stop": stop,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "logprobs": logprobs,
            "stream": stream,
            "logit_bias": logit_bias,
            "top_logprobs": top_logprobs,
            "response_format": response_format,
            "seed": seed,
            "stream_options": stream_options,
            "tools": tools,
            "tool_choice": tool_choice,
            "user": user,
        }

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        response = openai.chat.completions.create(**kwargs)

        return response.choices[0].message.content.strip()