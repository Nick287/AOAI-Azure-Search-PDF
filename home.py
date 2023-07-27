import streamlit as st
from function.AzureVectorSearch import AzureVectorSearch


azureVectorSearch = AzureVectorSearch()
index_name = 'surfacepro9-index-001'

st.title('Please input your question and press enter to search:')
prompt = st.text_input('please input your question')
# If the user hits enter
if prompt:
    with st.spinner(text="Document Searching..."):
        queary = prompt
        vector_fields = "contentVector"
        azureVectorSearch = AzureVectorSearch()
        results = azureVectorSearch.vector_similarity_search(index_name,vector_fields,queary)
        index = 1
        for result in results:
            st.write(f"################################### # {index} data ######################################")  
            st.write(f"content: {result['content']}")  
            st.write(f"Score: {result['@search.score']}")
            st.write(f"customer: {result['product']}")  
            st.write(f"Category: {result['category']}\n")  
            index = index + 1
    st.success("done!")