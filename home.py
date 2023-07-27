import streamlit as st
from function.AzureVectorSearch import AzureVectorSearch

# Build a prompt to provide the original query, the result and ask to summarise for the user
retrieval_prompt = '''Use the content to answer the search query the customer has sent.
If you can't answer the user's question, say "Sorry, I am unable to answer the question with the content". Do not guess.

Search query: 

SEARCH_QUERY_HERE

Content: 

SEARCH_CONTENT_HERE

Answer:
'''

azureVectorSearch = AzureVectorSearch()
index_names = azureVectorSearch.list_index_names()
# index_name = 'surfacepro9-index-001'
st.title('Please input your question and press enter to search:')

option = st.selectbox('How would you like to be contacted index?',index_names)
st.write('You selected:', option)
index_name = option

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
        complet_result = azureVectorSearch.openAI_ChatCompletion(retrieval_prepped)
        st.write(f"{complet_result}\n\n")

    st.success("done!")