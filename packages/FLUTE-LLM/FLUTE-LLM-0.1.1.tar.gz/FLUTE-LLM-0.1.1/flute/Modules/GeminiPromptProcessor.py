# GeminiPromptProcessor.py

from typing import List, Union, Optional
from AbstractPromptProcessor import AbstractPromptProcessor

try:
    import google.generativeai as genai
    import google.generativeai.types as genai_types
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    import google.ai.generativelanguage as genai_lang
except ImportError:
    genai = None

class GeminiPromptProcessor(AbstractPromptProcessor):
    def __init__(self, api_key: Optional[str] = None, model: str = "models/gemini-1.5-flash-latest"):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def generate_response(
        self,
        prompt: Union[str, List[str]],
        *,
        model: Optional[str] = "models/gemini-1.5-flash-latest",
        max_tokens: Optional[int] = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        top_k: int = 1,
        n: int = 1,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
        system: Optional[str] = None,
        # Gemini specific arguments
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            # Not supported in Gemini models
            # HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
            # HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
            # HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
            # HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE,
            # HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
            # HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
            # HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
        },
        generation_config: Optional[genai.GenerationConfig] = None,
        tools: Optional[genai_types.FunctionLibrary] = None,
        tool_config: Optional[genai_lang.ToolConfig] = None,
    ) -> Union[str, List[str]]:
        if genai is None:
            raise ImportError("The 'google.generativeai' library is not installed. Please install it to use GeminiPromptProcessor.")
        
        if model is not None or system is not None:
            self.model = genai.GenerativeModel(model, system_instruction=super().remove_special_characters(system))

        contents = []
        if isinstance(prompt, str):
            contents.append(super().remove_special_characters(prompt))
        else:
            contents.extend([super().remove_special_characters(p) for p in prompt])

        if generation_config is None:
            generation_config = genai.GenerationConfig(
                    candidate_count=n,
                    stop_sequences=stop,
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
            )

        response = self.model.generate_content(
            contents=contents,
            stream=stream,
            safety_settings=safety_settings,
            generation_config=generation_config,
            tools=tools,
            tool_config=tool_config,
        )

        return response.text