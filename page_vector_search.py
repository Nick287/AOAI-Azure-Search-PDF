import streamlit as st
#from function.AzureVectorSearch import AzureVectorSearch
from function.ChromaHelper import ChromaHelper
from langchain.llms import LlamaCpp

LLM_N_THREADS = 32
system_meg = """
You are an AI assistant that helps people find information. first, you can search the private data content to get the answer, if there's no avaiable information, then check your base model to return the reasonable information.
"""

# If you can't answer the user's question, say "Sorry, I am unable to answer the question with the content". Do not guess.
# Build a prompt to provide the original query, the result and ask to summarise for the user
# retrieval_prompt = '''Use the content to answer the search query the customer has sent.
# If the content can not answer the user's question, please provide a reasonable answer.

# Search query: 

# SEARCH_QUERY_HERE

# Content: 

# SEARCH_CONTENT_HERE

# Answer:
# '''
retrieval_prompt = '''Use the Content to answer the Search Query.

Search Query: 

SEARCH_QUERY_HERE

Content: 

SEARCH_CONTENT_HERE

Answer:
'''
st.title('Please input your question and press enter to search:')
#azureVectorSearch = AzureVectorSearch()
model = LlamaCpp(model_path="./models/llama-2-7b.Q4_K_M.gguf", verbose=True, n_threads=LLM_N_THREADS)
# chromaHelper = ChromaHelper()

with st.spinner(text="Loading..."):
    chromaHelper = ChromaHelper()
    index_names = chromaHelper.list_index_names()
    # index_names = azureVectorSearch.list_index_names()
    index_name = st.selectbox('Please select an index name.',index_names)
    st.write('You selected:', index_name)

prompt = st.text_input('please input your question')
# If the user hits enter
if prompt:
    with st.spinner(text="Document Searching..."):
        vector_fields = "contentVector"
        # azureVectorSearch = AzureVectorSearch()
        # results = azureVectorSearch.vector_similarity_search(index_name,vector_fields,prompt)

        chromaHelper = ChromaHelper()
        results = chromaHelper.similarity_search(index_name,prompt)

        index = 1
        search_content = ""


        with st.expander(f"Search Content History"):
            documents = results["documents"][0]
            for doc in documents:
                st.info(f"############################# # {index} data ################################") 
                st.info(f"content: {doc}")  
                index = index + 1
                search_content += doc + "\n"
        # with st.expander(f"Search Content History"):
        #     for result in results:
        #         st.info(f"############################# # {index} data ################################")  
        #         st.info(f"content: {result['content']}")  
        #         st.info(f"Score: {result['@search.score']}")
        #         st.info(f"customer: {result['product']}")  
        #         st.info(f"Category: {result['category']}\n")  
        #         index = index + 1
        #         search_content += result['content'] + "\n"

        retrieval_prepped = retrieval_prompt.replace('SEARCH_QUERY_HERE',prompt).replace('SEARCH_CONTENT_HERE',search_content)
        st.write(f"{retrieval_prepped}\n\n")

        complet_result = model(retrieval_prepped)
        #complet_result = azureVectorSearch.openAI_ChatCompletion(system_meg, retrieval_prepped)
        #st.write(f"This is llama2 results\n")
        st.write(f"{complet_result}\n\n")
    # st.success("done!")
