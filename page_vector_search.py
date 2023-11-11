import streamlit as st

from function.vectory_db_helper.vectory_db_factory import *
from function.abstract_vectory_db.vectory_db import *
from function.openai_helper.openai_function import *
from function.openai_helper.prompt_meg import *

vectory_db = vectory_db_factory().create_vectory_db(vectory_db_type.chroma_db)
openai_client = openai_helper(openai_type.azure)

st.title('Please input your question and press enter to search:')
with st.spinner(text="Loading..."):
    index_names = vectory_db.list_index_names()
    index_name = st.selectbox('Please select an index name.',index_names)
    st.write('You selected:', index_name)

prompt = st.text_input('please input your question')
# If the user hits enter
if prompt:
    with st.spinner(text="Document Searching..."):
        vector_fields = "contentVector"
        results = vectory_db.similarity_search(index_name,prompt)

        index = 1
        search_content = ""

        with st.expander(f"Search Content History"):
            documents = results["documents"][0]
            for doc in documents:
                st.info(f"############################# # {index} data ################################") 
                st.info(f"content: {doc}")  
                index = index + 1
                search_content += doc + "\n"

        retrieval_prepped = retrieval_prompt.replace('SEARCH_QUERY_HERE',prompt).replace('SEARCH_CONTENT_HERE',search_content)
        complet_result = openai_client.openAI_ChatCompletion(system_meg, retrieval_prepped)
        st.write(f"{complet_result}\n\n")
    # st.success("done!")