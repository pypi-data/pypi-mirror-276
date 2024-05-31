from abc import ABC, abstractmethod
from typing import List, Union, Optional
from dotenv import load_dotenv
import os

class AbstractPromptProcessor(ABC):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self._api_key = api_key

    @abstractmethod
    def generate_response(
        self,
        prompt: Union[str, List[str]],
        *,
        model: str,
        max_tokens: Optional[int] = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        n: int = 1,
        stop: Optional[Union[str, List[str]]] = None,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        logprobs: Optional[int] = None,
        stream: bool = False,
        system: Optional[str] = None,
    ) -> Union[str, List[str]]:
        """
        Generate a response from the language model.

        Args:
            prompt: The input prompt or a list of prompts.
            model: The name of the model to use.
            max_tokens: The maximum number of tokens to generate.
            temperature: The sampling temperature for controlling randomness.
            top_p: The cumulative probability threshold for nucleus sampling.
            n: The number of responses to generate.
            stop: The stopping sequence(s) for generation.
            presence_penalty: The penalty for repeated tokens.
            frequency_penalty: The penalty for frequent tokens.
            logprobs: The number of logprobs to return.
            stream: Whether to stream the response.
            system: System Prompt.

        Returns:
            The generated response or a list of responses.
        """
        pass

    @property
    def api_key(self) -> str:
        """Get the API key."""
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        """Set the API key."""
        self._api_key = value

    def load_api_key(self, env_var: str):
        """
        Load the API key from an environment variable using dotenv.

        Args:
            env_var: The name of the environment variable containing the API key.
        """
        load_dotenv()
        self._api_key = os.getenv(env_var)
        if self._api_key is None:
            raise ValueError(f"API key not found in environment variable {env_var}")
        
    def remove_special_characters(self, text):
        if text is None:
            return text
        text = text.replace("<|", "")
        text = text.replace("|>", "")
        return text