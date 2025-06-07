from google.genai import types
from google import genai
from GeminiLLM import GeminiLLM

class GeminiTools():
    def __init__(self, geminillm:GeminiLLM, result= None):
        self.geminillm = geminillm
        self.result =  result
        self.gemini_thinking_declaration = {
            "name": "GeminiThinking",
            "description": (
                "This declaration is used to enable the 'Thinking Tool' functionality within the Gemini client. "
                "When a user explicitly requests the system to enter thinking mode, this schema structures the "
                "parameters required to process and handle that request appropriately."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "The exact textual input provided by the user, representing the query or statement "
                            "that the system will process while operating in thinking mode."
                        ),
                    },
                    "trigger": {
                        "type": "string",
                        "enum": ["True"],
                        "description": (
                            "A fixed flag indicating that the thinking mode is active. This parameter is always "
                            "set to the string value 'True' to signify that the system should engage in enhanced "
                            "cognitive processing as requested by the user."
                        ),
                    },
                },
                "required": ["query", "trigger"],
            },
        }
        
        self.google_search_tool = {
            "name": "GoogleSearchTool",
            "description": "A tool that performs direct searches on the Google search engine.",
            "parameters": {
                "type": "object",
                "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query you want to look up on Google."
                }
                },
                "required": ["query"]
            }
        }

        self.gemini_code_execution_tool = {
            "name": "GeminiCodeExecutionTool",
            "description": "A tool only for Coding, google code execution tool",
            "parameters": {
                "type": "object",
                "properties": {
                "query": {
                    "type": "string",
                    "description": "The user asked query, on which code is to be written."
                }
                },
                "required": ["query"]
            }
        }
        # Set up tools and config with the function declaration
        self.tools = types.Tool(function_declarations=[self.gemini_thinking_declaration,  self.google_search_tool, self.gemini_code_execution_tool])
        self.config = types.GenerateContentConfig(tools=[self.tools])

    def generate_thinking_mode_response(self, prompt_text: str):
        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=prompt_text)]
            )
        ]

        response = self.geminillm.client.models.generate_content(
            model=self.geminillm.model_id,
            config=self.config,
            contents=contents
        )

        self.result = response

        return self.result
    
# geminillm = GeminiLLM()
# gemini_tools = GeminiTools(geminillm=geminillm)
# # prompt = "Thinkmode on/n/n WHat is AI."
# # prompt = "WHat is AI."
# prompt = "How do you compute the nth Fibonacci number using memoization in one line?"
# result = gemini_tools.generate_thinking_mode_response(prompt)
# print(result)
# print(len(result.candidates[0].content.parts))
# print((result.candidates[0].content.parts[0].function_call))