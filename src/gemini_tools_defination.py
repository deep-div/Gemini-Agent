from google.genai import types
from google import genai
from gemini_llm import GeminiLLM

class GeminiToolDefination:
    def __init__(self, geminillm: GeminiLLM, result=None):
        self.geminillm = geminillm
        self.result = result

        self.gemini_thinking_declaration = {
            "name": "GeminiThinking",
            "description": (
                "Use this tool when the user's input suggests they are looking for thoughtful reflection, brainstorming, "
                "hypothetical reasoning, or deep analysis. This includes philosophical questions, complex scenarios, or tasks "
                "where the agent must 'think' or 'reflect' to provide a structured or creative response. "
                "When to use: if the user is asking 'what if', 'analyze', 'brainstorm', or 'explore possibilities'. "
                "Avoid this tool for factual, time-sensitive, or technical queries—use search or code tools instead."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "Queries asking for reasoning or deep thought. "
                            "Examples: 'What are some possible futures if humans colonize Mars?', "
                            "'Can you explore the societal effects of AI on human creativity?', "
                            "'Is ambition more helpful or harmful in life?'"
                        )
                    }
                },
                "required": ["query"]
            }
        }

        self.google_search_tool = {
            "name": "GoogleSearchTool",
            "description": (
                "Use this tool when the user is asking for specific, real-time, or factual information that may be outside the model's knowledge. "
                "This includes recent news, live events, product prices, names, or anything the model cannot confidently answer from training data alone. "
                "When to use: if the model would otherwise respond with 'I'm not sure', 'As of my last update', or 'I cannot browse the web'. "
                "Avoid this for reasoning or general knowledge that doesn't need live updates."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "Use for fact-seeking or current-event queries. "
                            "Examples: 'What is the weather in Delhi today?', 'Latest iPhone 16 release date in India', "
                            "'Who is the current CEO of Google?', 'How did the 2024 elections end?'"
                        )
                    }
                },
                "required": ["query"]
            }
        }

        self.gemini_code_execution_tool = {
            "name": "GeminiCodeExecutionTool",
            "description": (
                "Use this tool when the user's prompt involves programming—writing, debugging, explaining, or executing code. "
                "Only invoke this for well-scoped technical/code tasks that require functional accuracy or output simulation. "
                "When to use: if the user asks for code generation, debugging, implementation, or syntax correction. "
                "Avoid this for general tech explanations—those don't require execution."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "Programming-related prompts. "
                            "Examples: 'Write a Python function to reverse a list', 'Fix this error in my code: ...', "
                            "'What will this JavaScript function return?', 'Create a REST API in Flask'."
                        )
                    }
                },
                "required": ["query"]
            }
        }

        self.tools = types.Tool(function_declarations=[
            self.gemini_thinking_declaration,
            self.google_search_tool,
            self.gemini_code_execution_tool
        ])

        self.config = types.GenerateContentConfig(tools=[self.tools])

    def pick_the_tool(self, prompt_text: str):
        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=prompt_text)]
            )
        ]

        try:
            response = self.geminillm.client.models.generate_content(
                model=self.geminillm.model_id,
                config=self.config,
                contents=contents
            )
            self.result = response
            return self.result
        except Exception as e:
            raise RuntimeError(f"Failed to generate response with tools: {str(e)}")
