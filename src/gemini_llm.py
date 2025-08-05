import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class GeminiLLM:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_Key")
        if not self.api_key:
            raise ValueError("API key must be provided or set in the environment variable 'GEMINI_API_Key'")
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini client: {str(e)}")
        self.model_id = "gemini-2.0-flash"

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
            )
            if hasattr(response, "text"):
                return response.text
            raise RuntimeError("No response text received from model")
        except Exception as e:
            raise RuntimeError(f"Error generating response: {str(e)}")

    def stream_response(self, prompt: str):
        try:
            stream = self.client.models.generate_content_stream(
                model=self.model_id,
                contents=prompt,
            )
            for chunk in stream:
                if hasattr(chunk, "text") and chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error during streaming: {str(e)}"
