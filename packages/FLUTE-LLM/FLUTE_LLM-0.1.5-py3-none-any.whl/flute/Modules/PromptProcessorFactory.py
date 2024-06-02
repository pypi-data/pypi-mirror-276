# PromptProcessorFactory.py

from typing import Optional
from dotenv import load_dotenv
import os

import flute
from flute.Modules.AbstractPromptProcessor import AbstractPromptProcessor
from flute.Modules.ClaudePromptProcessor import ClaudePromptProcessor
from flute.Modules.GPTPromptProcessor import GPTPromptProcessor
from flute.Modules.GeminiPromptProcessor import GeminiPromptProcessor

class PromptProcessorFactory:
    @staticmethod
    def create_prompt_processor(model_name: str, api_key: Optional[str] = None):
        if api_key is None:
            load_dotenv()

        if model_name in [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
        ]:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            return ClaudePromptProcessor(api_key=api_key, model=model_name)
        elif model_name in [
            "gpt-4o",
            "gpt-4o-2024-05-13",
            "gpt-4-turbo",
            "gpt-4-turbo-2024-04-09",
            "gpt-4-turbo-preview", 
            "gpt-4-0125-preview",
            "gpt-4-1106-preview",
            "gpt-4-vision-preview",
            "gpt-4-1106-vision-preview",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
        ]:
            api_key = os.getenv("OPENAI_API_KEY")
            return GPTPromptProcessor(api_key=api_key)
        elif model_name in [
            "gemini-1.5-pro-latest", 
            "gemini-1.5-flash-latest",
            "gemini-1.0-pro",
            "gemini-pro-vision",
            "models/gemini-1.5-pro-latest", 
            "models/gemini-1.5-flash-latest",
            "models/gemini-1.0-pro",
            "models/gemini-pro-vision",
        ]:
            api_key = os.getenv("GOOGLE_API_KEY")
            return GeminiPromptProcessor(api_key=api_key, model=model_name)
        ## TODO: Groq, Local LLMs, Brain Computer Interface, etc...
        else:
            return None