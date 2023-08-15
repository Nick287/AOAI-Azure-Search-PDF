import streamlit as st
from function.AzureVectorSearch import AzureVectorSearch

system_meg = """
You are an AI assistant that helps people find information. first, you can search the private data content to get the answer, if there's no avaiable information, then check your base model to return the reasonable information.
"""

# Build a prompt to provide the original query, the result and ask to summarise for the user
retrieval_prompt = '''Use the content to answer the search query the customer has sent.
If the content can not answer the user's question, please provide a reasonable answer.

Search query: 

SEARCH_QUERY_HERE

Content: 

SEARCH_CONTENT_HERE

Answer:
'''

st.title('Please input your question and press enter to search:')
azureVectorSearch = AzureVectorSearch()

with st.spinner(text="Loading..."):
    index_names = azureVectorSearch.list_index_names()
    index_name = st.selectbox('Please select an index name.',index_names)
    st.write('You selected:', index_name)

prompt = st.text_input('please input your question')
# If the user hits enter
if prompt:
    with st.spinner(text="Document Searching..."):
        vector_fields = "contentVector"
        azureVectorSearch = AzureVectorSearch()
        results = azureVectorSearch.vector_similarity_search(index_name,vector_fields,prompt)
        index = 1
        search_content = ""

        with st.expander(f"Search Content History"):
            for result in results:
                st.info(f"############################# # {index} data ################################")  
                st.info(f"content: {result['content']}")  
                st.info(f"Score: {result['@search.score']}")
                st.info(f"customer: {result['product']}")  
                st.info(f"Category: {result['category']}\n")  
                index = index + 1
                search_content += result['content'] + "\n"

        retrieval_prepped = retrieval_prompt.replace('SEARCH_QUERY_HERE',prompt).replace('SEARCH_CONTENT_HERE',search_content)
        complet_result = azureVectorSearch.openAI_ChatCompletion(system_meg, retrieval_prepped)
        st.write(f"{complet_result}\n\n")
    # st.success("done!")