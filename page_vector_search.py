import streamlit as st

from function.vectory_db_helper.vectory_db_factory import *
from function.abstract_vectory_db.vectory_db import *
from function.openai_helper.openai_function import *
from function.openai_helper.prompt_meg import *
from app_config.keys_config import *
from app_config.website_config import *

vectory_db = vectory_db_factory().create_vectory_db(DB_TYPE)
openai_client = openai_helper(AI_TYPE)

st.title('Please input your question:')
with st.spinner(text="Loading..."):
    index_names = vectory_db.list_index_names()
    index_name = st.selectbox('Please select an index name.',index_names)
    st.write('You selected:', index_name)

from azure.storage.blob import generate_account_sas, ResourceTypes, AccountSasPermissions
from datetime import datetime, timedelta, timezone

def prepare_sas_blob_url(storage_account: str,
                         account_key: str,
                         container: str,
                         file_name: str) -> str:
    """ Prepare SAS blob URL
    """
    start_time = datetime.now(timezone.utc)

    sas_token = generate_account_sas(
        account_name=storage_account,
        account_key=account_key,
        resource_types=ResourceTypes(object=True),
        permission=AccountSasPermissions(read=True),
        start=start_time,
        expiry=start_time + timedelta(minutes=30)
    )

    # Create blob SAS URL
    blob_sas_url = f"https://{storage_account}.blob.core.windows.net/{container}/{file_name}?{sas_token}"
    return blob_sas_url


prompt = st.text_input('please input your question')
# If the user hits enter
if prompt:
    with st.spinner(text="Thinking..."):
        vector_fields = "contentVector"
        results = vectory_db.similarity_search(index_name,prompt)

        index = 1
        search_content = ""

        with st.expander(f"Search Content History"):
            for result in results:
                st.info(f"############################# # {index} data ################################")

                SOURCE_PDF_FILE_PATH = result['file_name']
                STORAGE_ACCOUNT = "testopenaistorage001"
                TOKEN = ""
                CONTAINER_NAME = "pdf"
                pdf_blob_sas_url = prepare_sas_blob_url(STORAGE_ACCOUNT, TOKEN, CONTAINER_NAME, SOURCE_PDF_FILE_PATH)+ f"#page={result['page_num']}"

                st.info(f"content: {result['content']}")  
                st.info(f"page num: {result['page_num']}")  
                st.info(f"file name: {result['file_name']}") 
                st.info(f"[reference page: {result['page_num']}]({pdf_blob_sas_url})")
                st.info(f"Score: {result['@search.score']}")
                index = index + 1
                search_content += str(result['content']) + "\n"  

        retrieval_prepped = retrieval_prompt.replace('SEARCH_QUERY_HERE',prompt).replace('SEARCH_CONTENT_HERE',search_content)
        complet_result = openai_client.openAI_ChatCompletion(system_meg, retrieval_prepped)
        st.write(f"{complet_result}\n\n")
    # st.success("done!")