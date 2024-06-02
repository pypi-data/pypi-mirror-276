# test_prompt_processors.py

import pytest
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Modules'))

from PromptProcessorFactory import PromptProcessorFactory

load_dotenv()

def test_create_claude_prompt_processor():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    processor = PromptProcessorFactory.create_prompt_processor("claude-3-haiku-20240307", api_key=api_key)
    assert processor.api_key == api_key
    assert processor.model == "claude-3-haiku-20240307"

    response = processor.generate_response("Hello, how are you?", max_tokens=4096, temperature=1.0, top_p=1, system="You are an assistant")
    assert isinstance(response, str)

def test_create_claude_prompt_processor_without_api_key():
    processor = PromptProcessorFactory.create_prompt_processor("claude-3-haiku-20240307")
    assert processor.model == "claude-3-haiku-20240307"

    response = processor.generate_response("Hello, how are you?", max_tokens=4096, temperature=1.0, top_p=1, system="You are an assistant")
    assert isinstance(response, str)

def test_create_gpt_prompt_processor():
    api_key = os.getenv("OPENAI_API_KEY")
    processor = PromptProcessorFactory.create_prompt_processor("gpt-4o", api_key=api_key)
    assert processor.api_key == api_key

    response = processor.generate_response("Hello, how are you?", model="gpt-4o", max_tokens=4096, temperature=1.0, top_p=1, system="You are an assistant")
    assert isinstance(response, str)

def test_create_gpt_prompt_processor_without_api_key():
    processor = PromptProcessorFactory.create_prompt_processor("gpt-4o")

    response = processor.generate_response("Hello, how are you?", model="gpt-4o", max_tokens=4096, temperature=1.0, top_p=1, system="You are an assistant")
    assert isinstance(response, str)

def test_create_gemini_prompt_processor():
    api_key = os.getenv("GOOGLE_API_KEY")
    processor = PromptProcessorFactory.create_prompt_processor("models/gemini-1.5-flash-latest", api_key=api_key)
    assert processor.api_key == api_key
    assert processor.model.model_name == "models/gemini-1.5-flash-latest"

    response = processor.generate_response("Hello, how are you?", max_tokens=4096, temperature=1.0, top_p=1, system="You are an assistant")
    assert isinstance(response, str)

def test_create_gemini_prompt_processor_without_api_key():
    processor = PromptProcessorFactory.create_prompt_processor("gemini-1.5-flash-latest")
    assert processor.model.model_name == "models/gemini-1.5-flash-latest"

    response = processor.generate_response("Hello, how are you?", max_tokens=4096, temperature=1.0, top_p=1, system="You are an assistant")
    assert isinstance(response, str)