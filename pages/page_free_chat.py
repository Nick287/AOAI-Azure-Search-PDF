from openai import OpenAI
from openai import AsyncAzureOpenAI
from openai import AzureOpenAI
import streamlit as st
import os

from navigation import make_sidebar
make_sidebar()

col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

with col1:
    chat_model = st.selectbox('Please select a chat model.', ["gpt-4o-mini", "gpt-4o"])

with col2:
    if st.button('Clean Chat History'):
        if 'free_messages' in st.session_state:
            del st.session_state['free_messages']
            st.rerun()

# # st.write('You selected:', chat_model)

client = AzureOpenAI(
    azure_endpoint="https://aoaieastus001.openai.azure.com/",
    api_key=os.environ["free-chat-4o-key"],
    api_version="2023-03-15-preview"
)

settings = {
    "model": chat_model,
    "temperature": 0.7,
    "max_tokens": 800,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

# Generate Stream
def stream_processor(response):
    for chunk in response:
        if len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content


if "free_messages" not in st.session_state:
    st.session_state.free_messages =  []

for message in st.session_state.free_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.free_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.free_messages ]
        history.insert(0, {"role": "system", "content": "You are an AI assistant that helps people find information."})
        stream = client.chat.completions.create(
            **settings,
            messages=history,
            stream=True,
        )
        response = st.write_stream(stream_processor(stream))
    st.session_state.free_messages.append({"role": "assistant", "content": response})