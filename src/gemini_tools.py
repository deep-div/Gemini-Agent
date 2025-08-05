from google.genai import types
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from gemini_llm import GeminiLLM
from bs4 import BeautifulSoup
import requests

class GeminiThinking:
    def __init__(self, geminillm: GeminiLLM, model_id="gemini-2.5-flash-preview-05-20"):
        self.geminillm = geminillm
        self.modelid = model_id

    def activate_stream(self, prompt: str):
        try:
            stream = self.geminillm.client.models.generate_content_stream(
                model=self.modelid,
                contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(include_thoughts=True)
                )
            )

            for chunk in stream:
                if not chunk.candidates:
                    continue

                for part in chunk.candidates[0].content.parts:
                    if hasattr(part, "thought") and part.thought:
                        yield {"text": part.text, "thought": True}
                    elif hasattr(part, "text") and part.text:
                        yield {"text": part.text, "thought": False}

        except Exception as e:
            yield {"text": f"Error during GeminiThinking stream: {str(e)}", "thought": False}


class GoogleSearchTool:
    def __init__(self, geminillm: GeminiLLM):
        self.geminillm = geminillm
        self.tool = Tool(google_search=GoogleSearch())
        self.response = None
        self.grounding = None

    def activate_stream(self, prompt: str):
        try:
            stream = self.geminillm.client.models.generate_content_stream(
                model=self.geminillm.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[self.tool],
                    response_modalities=["TEXT"]
                )
            )

            for chunk in stream:
                if not chunk.candidates:
                    continue

                candidate = chunk.candidates[0]
                self.grounding = candidate.grounding_metadata if hasattr(candidate, "grounding_metadata") else None

                for part in candidate.content.parts:
                    if hasattr(part, "text") and part.text:
                        yield part.text

        except Exception as e:
            yield f"Error during GoogleSearchTool stream: {str(e)}"

class GeminiCodeExecutionTool:
    def __init__(self, geminillm: GeminiLLM):
        self.geminillm = geminillm 

    def activate_stream(self, prompt: str):
        try:
            stream = self.geminillm.client.models.generate_content_stream(
                model=self.geminillm.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(code_execution=types.ToolCodeExecution())],  
                    response_modalities=["TEXT"]
                ),
            )

            for chunk in stream:
                if not chunk.candidates:
                    continue

                candidate = chunk.candidates[0]
                for part in candidate.content.parts:
                    if hasattr(part, "text") and part.text:
                        yield part.text
                    elif hasattr(part, "executable_code") and part.executable_code:
                        yield f"\n\n```python\n{part.executable_code.code}\n```\n"
                    elif hasattr(part, "code_execution_result") and part.code_execution_result:
                        yield f"\n\n**Output:**\n```\n{part.code_execution_result.output}\n```\n"

        except Exception as e:
            yield f"Error during code execution: {str(e)}"




