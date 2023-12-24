import openai
from llama_index.agent import OpenAIAgent
import streamlit as st
from llama_hub.tools.requests import RequestsToolSpec

openai_api_key = ""#Insert API Key
domain_headers = {
    "api.openai.com":{
        "Authorization": f"Bearer {openai_api_key}",
        "Content-type": "application/json"
    },
    '127.0.0.1': {
        "Content-Type": "application/json"
    }
}

weather_agent = RequestsToolSpec(domain_headers=domain_headers).to_tool_list()
openai.api_key = openai_api_key

system_prompt = "You're WeatherGPT, your goal is to tell me the weather based on the user input, when a user propts for the weather, make a GET api request to http://127.0.0.1:5000/weather?country=[TWO_DIGITS_COUNTRY_CODE]&city=[CITY] example: http://127..0.0.1:5000/weather?country=FR&city=Paris"

agent = OpenAIAgent.from_tools(weather_agent, system_prompts=system_prompt)

agent.chat_repl()

st.title("LLM Cool Chat UI")

if "agent" not in st.session_state:
    st.session_state.agent = agent

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Ask me anything"
        }
    ]

if prompt := st.chat_input("Your prompt"):
    st.session_state.messages.append({
        "role":"user",
        "content":prompt,
    })

# load all messages from the messages array
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.spinner("thinking..."):
        response = st.session_state.agent.chat(prompt)
        message = {
            "role": "assistant",
            "content": response.response
        }

    st.session_state.messages.append(message)
    with st.chat_message("assistant"):
        st.write(response.response)
