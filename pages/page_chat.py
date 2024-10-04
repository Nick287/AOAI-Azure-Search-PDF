from openai import OpenAI
from openai import AsyncAzureOpenAI
from openai import AzureOpenAI
import streamlit as st

from function.vectory_db_helper.vectory_db_factory import *
from function.abstract_vectory_db.vectory_db import *
from app_config.keys_config import *
from app_config.website_config import *
from function.openai_helper.prompt_meg import *

vectory_db = vectory_db_factory().create_vectory_db(DB_TYPE)

from navigation import make_sidebar
make_sidebar()

# st.title("Chat with your document")

gpt4o_mini_api_key = os.environ["temp-gpt-4o-mini-key"]

with st.spinner(text="Loading..."):
    index_names = vectory_db.list_index_names()
    index_name = st.selectbox('Please select an index name.',index_names)
    st.write('You selected:', index_name)

client = AzureOpenAI(
    azure_endpoint="https://openAIBo.openai.azure.com/",
    api_key=gpt4o_mini_api_key,
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
    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages ]
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if prompt:
        with st.spinner(text="Thinking..."):
            vector_fields = "contentVector"
            results = vectory_db.similarity_search(index_name,prompt)
            search_content = ""
            for result in results:
                search_content += str(result['content']) + "\n"
            retrieval_prepped = retrieval_prompt.replace('SEARCH_QUERY_HERE',prompt).replace('SEARCH_CONTENT_HERE',search_content)
            history.insert(0, {"role": "system", "content": system_meg})
            history.append({"role": "user", "content": retrieval_prepped})
            stream = client.chat.completions.create(
                **settings,
                messages=history,
                stream=True,
            )

    with st.chat_message("assistant"):
        response = st.write_stream(stream_processor(stream))
    st.session_state.messages.append({"role": "assistant", "content": response})