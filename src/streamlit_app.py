import streamlit as st
from google import genai
from google.genai import types
from gemini_tools_defination import GeminiToolDefination
from gemini_llm import GeminiLLM
from gemini_history import ConversationBuilder
from gemini_tools import GeminiCodeExecutionTool, GeminiThinking, GoogleSearchTool
from utils import get_typing_indicator_html
from gemini_tool_selector import GeminiToolSelector

geminillm=GeminiLLM()
geminitooldefination = GeminiToolDefination(geminillm)
conversationbuilder = ConversationBuilder()
geminitoolselector = GeminiToolSelector()
client = geminillm.client

if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model=geminillm.model_id, config=geminitooldefination.config)

if "messages" not in st.session_state:
    st.session_state.messages = []

# default message
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="images/ai.png"):
        st.markdown("👋 **Hi! I can help you think, code, or search real-time info. Just ask!**")

# Tool name map
tool_mapping = {
    "Auto": None,
    "Think": "GeminiThinking",
    "Search": "GoogleSearchTool",
    "Code": "GeminiCodeExecutionTool"
}

# display chat messages from history at every rerun  
for message in st.session_state.messages:
    avatar_path = (
        "images/person_15454011.png" if message["role"] == "user"
        else "images/ai.png"
    )
    with st.chat_message(message["role"], avatar=avatar_path):
        st.markdown(message["content"])

if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "Auto"

st.sidebar.title("Tools")
selected_tool = st.sidebar.selectbox(
    "Choose a tool:",
    options=list(tool_mapping.keys()),
    index=list(tool_mapping.keys()).index(st.session_state.selected_tool),
)

# Update the session state with current selection
st.session_state.selected_tool = selected_tool

prompt = st.chat_input("What is up?")
selected_tool_name = tool_mapping[st.session_state.selected_tool]


if prompt:
    try:
        # show user message
        with st.chat_message("user", avatar="images/person_15454011.png"):
            st.markdown(prompt)
        # Save user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # stream assistant response
        full_response = ""
        with st.chat_message("assistant", avatar="images/ai.png"):
            response_stream = st.session_state.chat.send_message_stream(prompt)
            response_placeholder = st.empty()
            
            if selected_tool_name:
                tool_args = {"query": prompt}
                full_response = geminitoolselector.handle_tool_response(selected_tool_name, tool_args, geminillm)
                # need to add response in chat history
                content_only_convo = conversationbuilder.build_with_content_only(full_response)
                st.session_state.chat.get_history().extend(content_only_convo)

            else:
                for chunk in response_stream:
                    if chunk.text is None:  # if response is None means a tool is hit
                        tool_name = chunk.candidates[0].content.parts[0].function_call.name
                        tool_args = chunk.candidates[0].content.parts[0].function_call.args

                        response_placeholder = st.empty()
                        
                        # handle tool response
                        streamed_output = geminitoolselector.handle_tool_response(tool_name, tool_args, geminillm)

                        full_response = streamed_output  
                        
                        # IMP..... add the response in the chathistory can see by st.session_state.chat.get_history() see complete history you will see the content is missing there and u can also more then one conttent
                        content_only_convo = conversationbuilder.build_with_content_only(full_response)
                        st.session_state.chat.get_history().extend(content_only_convo)
                        
                        # st.markdown(st.session_state.chat.get_history())  ## for reference how chat history is working
                    else:
                        full_response += chunk.text
                        response_placeholder.markdown(full_response + "")  # stream effect

        # save assistant message (load all the messages to show chat type view in UI )
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        # print(st.session_state.chat.get_history())  ## for reference how chat history is working

    except Exception as e:
        st.error(f"An error occurred: {e}")


# py -m  streamlit run streamlit_app.py