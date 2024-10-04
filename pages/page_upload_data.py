import streamlit as st
from io import BytesIO 
import pandas as pd
import numpy as np
import uuid

from function.NormalizeText import NormalizeText
from function.LangChainChunking import LangChanSplitter
from function.vectory_db_helper.vectory_db_factory import *
from function.abstract_vectory_db.vectory_db import *
from function.openai_helper.openai_function import *

from app_config.keys_config import *
from app_config.website_config import *

from function.document_intelligence import *

from navigation import make_sidebar
make_sidebar()

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings  
import io  

vectory_db = vectory_db_factory().create_vectory_db(DB_TYPE)

st.title('Upload PDF file to Azure AI Search')

with st.spinner(text="Loading..."):
    index_names = vectory_db.list_index_names()
    index_name = st.selectbox('Please select an index name.',index_names)
    st.write('You selected:', index_name)


def upload_pdf_to_blob_storage(connection_string, container_name, blob_name, pdf_bytes):  
    try:  
        # Create the BlobServiceClient object  
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)  
  
        # Create a blob client using the container and blob name.  
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)  
  
        # Define content settings with application/pdf content-type  
        content_settings = ContentSettings(content_type='application/pdf')  
  
        # Upload the pdf bytes to blob storage with content settings  
        blob_client.upload_blob(pdf_bytes, content_settings=content_settings)  
  
    except Exception as ex:  
        print('Exception:')  
        print(ex)  
  
uploaded_file = st.file_uploader("Please Choose a DPF file",type="pdf")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    pdf_file = BytesIO(bytes_data) 

    with st.spinner(text="Document uploading..."):
        pdf_file.seek(0)      
        # Upload the pdf to blob storage
        connection_string = ""
        container_name = "pdf"
        file_name = "files/"+uploaded_file.name
        # upload_pdf_to_blob_storage(connection_string, container_name, file_name, pdf_file)  
        
        os.environ['DOCUMENTINTELLIGENCECLIENT_ENDPOINT'] = "https://bodocumentintelligence001.cognitiveservices.azure.com/"
        os.environ['DOCUMENTINTELLIGENCECLIENT_KEY'] = "8721341d84ab448085fa9c62dcaf6739"

        document_intelligence_helper = document_intelligence()

        page_content_list = document_intelligence_helper.get_page_content_list(bytes_data)

        splitted_text_df = pd.DataFrame()
        page_num = 1
        for page_text in page_content_list:
            df = pd.DataFrame({'document': [page_text]})
            df = df.dropna()
            df['page_num'] = page_num
            df['file_name'] = uploaded_file.name
            df['id'] = df.apply(lambda x: str(uuid.uuid4()), axis=1)
            splitted_text_df = pd.concat([splitted_text_df, df], ignore_index=True)
            page_num += 1
        splitted_text_df["page_num"] = splitted_text_df["page_num"].astype(str)    

        df_array = np.array_split(splitted_text_df, len(splitted_text_df) // 50 + 1)  
        data_array_count = len(df_array)

        with st.expander(f"log info:"):
            st.info("total batch job: " + str(data_array_count))
            new_df_array = []
            current_job_numeber = 1
            for sub_df in df_array:
                st.info("working on: " + str(current_job_numeber) + "/" +str(data_array_count))
                vectory_db.upload_documents(index_name, sub_df)
                new_df_array.append(sub_df)
                current_job_numeber+=1

            new_df = pd.concat(new_df_array, axis=0, ignore_index=True) 
            st.info(str(len(new_df)) + " records uploaded.")
    st.success("done!")