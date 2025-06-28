from google.genai import types 
from GeminiLLM import GeminiLLM
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from bs4 import BeautifulSoup
import requests
from google.genai import types
from IPython.display import Markdown, display

class GeminiThinking():
    def __init__(self, geminillm:GeminiLLM ,model_id="gemini-2.5-flash-preview-05-20",):
        self.thoughts = ""
        self.answer = ""
        self.modelid = model_id
        self.geminillm = geminillm
        
    def activate(self, prompt: str, trigger: bool):
        if not trigger:
            print("Activation signal is False. GeminiThinking not started.")
            return

        print("GeminiThinking activated...")

        self.thoughts = ""
        self.answer = ""
        stream = self.geminillm.client.models.generate_content_stream(
            model=self.modelid,
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    include_thoughts=True
                )
            )
        )

        for chunk in stream:
            for part in chunk.candidates[0].content.parts:
                if not part.text:
                    continue
                elif part.thought:
                    if not self.thoughts:
                        print("Thoughts summary:")
                    print(part.text)
                    self.thoughts += part.text
                else:
                    if not self.answer:
                        print("Answer:")
                    print(part.text)
                    self.answer += part.text

    def get_result(self):
        return {
            "thoughts": self.thoughts,
            "answer": self.answer
        }
        


class GoogleSearchTool:
    def __init__(self, geminillm: GeminiLLM):
        self.geminillm = geminillm
        self.tool = Tool(google_search=GoogleSearch())
        self.response = None
        self.grounding = None

    def ask_question(self, prompt):
        self.response = self.geminillm.client.models.generate_content(
            model=self.geminillm.model_id,
            contents=prompt,
            config=GenerateContentConfig(
                tools=[self.tool],
                response_modalities=["TEXT"]
            )
        )
        self.grounding = self.response.candidates[0].grounding_metadata
        for each in self.response.candidates[0].content.parts:
            print(each.text)

    def extract_sources(self):
        if not self.grounding:
            print("No grounding metadata found.")
            return []

        soup = BeautifulSoup(self.grounding.search_entry_point.rendered_content, 'html.parser')
        links = soup.find_all('a')

        print("Extracted Sources and Final URLs:\n")
        resolved_links = []

        for link in links:
            text = link.text.strip()
            redirect_url = link.get('href', '')
            try:
                response = requests.get(redirect_url, allow_redirects=True, timeout=5)
                final_url = response.url
            except requests.RequestException as e:
                final_url = f"(Failed to resolve: {e})"
            print(f"{text}: {final_url}")
            resolved_links.append((text, final_url))


class GeminiCodeExecutionTool:
    def __init__(self, geminillm: GeminiLLM):
        self.geminillm = geminillm 
    def generate_and_execute(self, prompt: str):
        response = self.geminillm.client.models.generate_content(
            model=self.geminillm.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution=types.ToolCodeExecution)]
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            if part.executable_code is not None:
                print(part.executable_code.code)
            if part.code_execution_result is not None:
                print(part.code_execution_result.output)


