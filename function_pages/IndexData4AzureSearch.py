# Import os to set API key
import os
# Import OpenAI as main LLM service
from langchain. llms import OpenAI
# Bring in streamlit for UI/app interface
import streamlit as st
import openai
from function.NormalizeText import NormalizeText as nt

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.azuresearch import AzureSearch
# from langchain.embeddings import OpenAIEmbeddings

# Import PDF document loaders...there's other ones as well!
from langchain.document_loaders import PyPDFLoader
# Import chroma as the vector store
from langchain.vectorstores import Chroma

# Import vector store stuff
from langchain.agents. agent_toolkits import(
create_vectorstore_agent,
VectorStoreToolkit, VectorStoreInfo)

# Set APIkey for Azure OpenAI Service
API_KEY = "abd3ed676d1d443981237994429781c6"
RESOURCE_ENDPOINT = "https://botestopenai.openai.azure.com" 
CHAT_MODEL = "boTestGPT35"
Chat_COMPLETION_MODEL ="best_text"
EMBEDDING_MODEL = "text-embedding"
openai.api_type = "azure"
openai.api_key = API_KEY
openai.api_base = RESOURCE_ENDPOINT
OPENAI_API_VERSION = '2023-05-15'
openai.api_version = OPENAI_API_VERSION

pdf_file = "EmployeeHandbook/EmployeeHandbook_English1107.pdf"

st.title('Hello! You are indexing data into Azure cognitive service now.')
st.subheader('Please upload your PDF is:')
st.subheader(pdf_file)


with st.spinner(text="Loading PDF..."):
    # Create instance of OpenAI LLM
    # llm = OpenAI(engine=Chat_COMPLETION_MODEL, openai_api_key = API_KEY,temperature=0.9)

    # Create and load PDF Loader
    loader = PyPDFLoader (pdf_file)
    # Split pages from pdf
    pages = loader.load_and_split()

    text = nt()
    item_list =[]

    for page in pages:  
        pagesitems = text.normalize_text_to_page_item(page.page_content)
        for pagesitem in pagesitems:
            page_text = pagesitem.strip()
            if page_text == "":
                continue      
            line = text.normalize_text_to_itemtext(page_text)
            item_list.append(line)

    # item_list

    model: str = "text-embedding-ada-002"
    vector_store_address: str = "YOUR_AZURE_SEARCH_ENDPOINT"
    vector_store_password: str = "YOUR_AZURE_SEARCH_ADMIN_KEY"
    index_name: str = "ms-employee-handbook-en"

    embeddings = OpenAIEmbeddings(model = "text-embedding-ada-002",
                    deployment = EMBEDDING_MODEL,
                    openai_api_version = OPENAI_API_VERSION,
                    openai_api_base = RESOURCE_ENDPOINT,
                    openai_api_type = "azure",
                    openai_api_key = API_KEY,
                    chunk_size=1
                    )

st.success("done!")

# embeddings: OpenAIEmbeddings = OpenAIEmbeddings(model=model, chunk_size=1,openai_api_key = API_KEY)
AzureSearch = AzureSearch(
    azure_search_endpoint="https://boazuresearch.search.windows.net",
    azure_search_key="T2V5rv7qrtQAOCX9QfUQPtHFGDGtaN2DglnEB96OXDAzSeD1iQcW",
    index_name=index_name,
    embedding_function = embeddings.embed_query,
)
# AzureSearch.add_texts(item_list)

st.write(item_list)
