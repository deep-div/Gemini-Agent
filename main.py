from GeminiLLM import GeminiLLM
from Tool_GeminiThinking_AndMore import *
from ToolSelector import *


class GeminiToolsExecution():
    def __init__(self, geminithinker: GeminiThinking, geminillm: GeminiLLM, googlesearchtool: GoogleSearchTool, geminicodeexecutiontool: GeminiCodeExecutionTool, result, prompt):
        self.result = result
        self.geminithinker = geminithinker
        self.geminillm =geminillm
        self.googlesearchtool =googlesearchtool
        self.geminicodeexecutiontool = geminicodeexecutiontool
        self.user_query = prompt
        
    def tool_result_to_gemini(self):
        tool_results={}
        if self.result.candidates[0].content.parts[0].function_call!=None:
            for ind in range(len(self.result.candidates[0].content.parts)):
                tool_results[self.result.candidates[0].content.parts[ind].function_call.name] = self.result.candidates[0].content.parts[ind].function_call.args

            # print(tool_results)
            
            for key, value in tool_results.items():
                print("Tool Calling:", key,value)
                if key=="GeminiThinking":
                    user_query = value['query']
                    frontend_signal = value['trigger']
                    print(user_query)
                    self.geminithinker.activate(prompt=value['query'], trigger=frontend_signal)
                elif key=="GoogleSearchTool":
                    user_query = value['query']
                    print(user_query)
                    self.googlesearchtool.ask_question(prompt)
                    self.googlesearchtool.extract_sources()
                elif key=="GeminiCodeExecutionTool":
                    user_query = value['query']
                    print(user_query)
                    self.geminicodeexecutiontool.generate_and_execute(user_query)
        else:
            print(self.user_query)
            for token in self.geminillm.stream_response(self.user_query):
                print(token, end="", flush=True)


geminillm = GeminiLLM()
geminithinker = GeminiThinking(geminillm)
googlesearchtool = GoogleSearchTool(geminillm)
geminicodeexecutiontool = GeminiCodeExecutionTool(geminillm)


print("-----------------------------Tool Execution---------------------------------------")

# prompt = "Thinkmode Tool\n\n Query: WHat is AI."
prompt = "Google Web Search Tool \n\n. Query: What is today NIFTY 50 Price?"
# prompt = "No Tool to be Used \n\n. WHat is AI."
# prompt = "Code Execution Tool \n\n Query: How do you compute the nth Fibonacci number using memoization in one line?"
gemini_tools = GeminiTools(geminillm=geminillm)
result = gemini_tools.generate_thinking_mode_response(prompt)
gemini_tools_execution = GeminiToolsExecution(geminithinker, geminillm, googlesearchtool, geminicodeexecutiontool, result=result, prompt=prompt)
gemini_tools_execution.tool_result_to_gemini()