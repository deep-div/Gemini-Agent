import streamlit as st
from google import genai
from google.genai import types
from gemini_tools import GeminiCodeExecutionTool, GeminiThinking, GoogleSearchTool
from utils import get_typing_indicator_html

class GeminiToolSelector():
    def __init__(self) -> None:
        pass

    def handle_tool_response(self, tool_name, tool_args, geminillm):
        if tool_name == "GeminiThinking":
            gen = GeminiThinking(geminillm).activate_stream(tool_args['query'])
            typing_placeholder = st.empty()
            thought_placeholder = st.empty()
            response_placeholder = st.empty()

            thought_buffer = ""
            streamed_output = ""

            typing_placeholder.markdown(get_typing_indicator_html("Thinking"), unsafe_allow_html=True)

            for chunk in gen:
                if chunk["thought"]:
                    thought_buffer += chunk["text"] + "\n"
                    with thought_placeholder.expander("Thoughts (click to expand)", expanded=False):
                        st.markdown(thought_buffer)
                else:
                    break

            typing_placeholder.empty()

            if chunk and not chunk["thought"]:
                streamed_output += chunk["text"]
                response_placeholder.markdown(streamed_output)

            for chunk in gen:
                if not chunk["thought"]:
                    streamed_output += chunk["text"]
                    response_placeholder.markdown(streamed_output)

            return streamed_output

        elif tool_name == "GoogleSearchTool":
            gen = GoogleSearchTool(geminillm).activate_stream(tool_args['query'])
            typing_placeholder = st.empty()
            typing_placeholder.markdown(get_typing_indicator_html("Searching Web"), unsafe_allow_html=True)
            response_placeholder = st.empty()

            try:
                first_chunk = next(gen)
            except StopIteration:
                first_chunk = ""

            typing_placeholder.empty()
            streamed_output = first_chunk
            response_placeholder.markdown(streamed_output)

            for chunk in gen:
                streamed_output += chunk
                response_placeholder.markdown(streamed_output)

            return streamed_output

        elif tool_name == "GeminiCodeExecutionTool":
            gen = GeminiCodeExecutionTool(geminillm).activate_stream(tool_args['query'])
            typing_placeholder = st.empty()
            typing_placeholder.markdown(get_typing_indicator_html("Writing Code"), unsafe_allow_html=True)
            response_placeholder = st.empty()

            try:
                first_chunk = next(gen)
            except StopIteration:
                first_chunk = ""

            typing_placeholder.empty()
            streamed_output = first_chunk
            response_placeholder.markdown(streamed_output)

            for chunk in gen:
                streamed_output += chunk
                response_placeholder.markdown(streamed_output)

            return streamed_output

        else:
            return "Unknown tool triggered."
