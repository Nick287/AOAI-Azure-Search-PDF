from openai import OpenAI
from openai import AsyncAzureOpenAI
from openai import AzureOpenAI
import streamlit as st

st.title("Conversation RAG")

client = AzureOpenAI(
    azure_endpoint="https://openAIBo.openai.azure.com/",
    api_key="",
    api_version="2024-02-15-preview"
)

settings = {
    "model": "gpt-4o-mini",
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


if "messages" not in st.session_state:
    st.session_state.messages =  []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages ]
        history.insert(0, {"role": "system", "content": "You are an AI assistant that helps people find information."})
        stream = client.chat.completions.create(
            **settings,
            messages=history,
            stream=True,
        )
        response = st.write_stream(stream_processor(stream))
    st.session_state.messages.append({"role": "assistant", "content": response})