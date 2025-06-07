import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

class GeminiLLM:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_Key")
        if not self.api_key:
            raise ValueError("API key must be provided or set in the environment variable 'GEMINI_API_Key'")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-2.0-flash"

    def generate_response(self, prompt: str) -> str:
        # Standard non-streaming response
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def stream_response(self, prompt: str):
        # Streaming response: yields each chunk of text as it's generated.
        try:
            stream = self.client.models.generate_content_stream(
                model=self.model_id,
                contents=prompt,
            )
            for chunk in stream:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error during streaming: {str(e)}"
