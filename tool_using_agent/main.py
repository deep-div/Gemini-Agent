from fastapi import FastAPI
from pydantic import BaseModel
from GeminiLLM import GeminiLLM
from Tool_GeminiThinking_AndMore import *
from ToolSelector import *
import io
import sys

# FastAPI app initialization
app = FastAPI()

# Request model
class PromptRequest(BaseModel):
    prompt: str


# Tool Execution class
class GeminiToolsExecution():
    def __init__(self, geminithinker: GeminiThinking, geminillm: GeminiLLM, googlesearchtool: GoogleSearchTool, geminicodeexecutiontool: GeminiCodeExecutionTool, result, prompt):
        self.result = result
        self.geminithinker = geminithinker
        self.geminillm = geminillm
        self.googlesearchtool = googlesearchtool
        self.geminicodeexecutiontool = geminicodeexecutiontool
        self.user_query = prompt
        
    def tool_result_to_gemini(self):
        tool_results = {}
        if self.result.candidates[0].content.parts[0].function_call is not None:
            for ind in range(len(self.result.candidates[0].content.parts)):
                part = self.result.candidates[0].content.parts[ind]
                tool_results[part.function_call.name] = part.function_call.args

            for key, value in tool_results.items():
                print("Tool Calling:", key, value)
                if key == "GeminiThinking":
                    user_query = value['query']
                    frontend_signal = value['trigger']
                    print(user_query)
                    self.geminithinker.activate(prompt=user_query, trigger=frontend_signal)
                elif key == "GoogleSearchTool":
                    user_query = value['query']
                    print(user_query)
                    self.googlesearchtool.ask_question(user_query)
                    self.googlesearchtool.extract_sources()
                elif key == "GeminiCodeExecutionTool":
                    user_query = value['query']
                    print(user_query)
                    self.geminicodeexecutiontool.generate_and_execute(user_query)
        else:
            print(self.user_query)
            for token in self.geminillm.stream_response(self.user_query):
                print(token, end="", flush=True)


# Initialize tools once
geminillm = GeminiLLM()
geminithinker = GeminiThinking(geminillm)
googlesearchtool = GoogleSearchTool(geminillm)
geminicodeexecutiontool = GeminiCodeExecutionTool(geminillm)
gemini_tools = GeminiTools(geminillm=geminillm)


# API endpoint
@app.post("/run-tools/")
def run_tools(request: PromptRequest):
    prompt = request.prompt

    # Generate result using ToolSelector
    result = gemini_tools.generate_thinking_mode_response(prompt)

    # Prepare execution class
    gemini_tools_execution = GeminiToolsExecution(
        geminithinker=geminithinker,
        geminillm=geminillm,
        googlesearchtool=googlesearchtool,
        geminicodeexecutiontool=geminicodeexecutiontool,
        result=result,
        prompt=prompt
    )

    # Capture stdout
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    # Execute
    gemini_tools_execution.tool_result_to_gemini()

    # Restore stdout and get output
    sys.stdout = old_stdout
    output = new_stdout.getvalue()

    return {"output": output}


