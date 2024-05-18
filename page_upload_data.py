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
        upload_pdf_to_blob_storage(connection_string, container_name, file_name, pdf_file)  
        
        # read pdf file
        pdf_reader = NormalizeText()
        longtxt_list = pdf_reader.get_doc_content_txt_v2(pdf_file,file_name)

        pdf_reader = LangChanSplitter()

        splitted_text_list = []
        for longtxt in longtxt_list:
            splitted_text = {}
            splitted_text["splitted_page_content"] = pdf_reader.TokenTextSplitter(300, 100, longtxt["content"])
            splitted_text["splitted_page_num"] = longtxt["page_num"]
            splitted_text["file_name"] = longtxt["file_name"]
            splitted_text_list.append(splitted_text)

        # stirnglist = pdf_reader.TokenTextSplitter(300,100,longtxt)

        # df = pd.DataFrame({'document': stirnglist})
        # df = df.dropna() 
        # df['id'] = df.apply(lambda x : str(uuid.uuid4()), axis=1)  


        splitted_text_df = pd.DataFrame()
        for splitted_page_text in splitted_text_list:
            df = pd.DataFrame({'document': splitted_page_text["splitted_page_content"]})
            df = df.dropna()
            df['page_num'] = splitted_page_text["splitted_page_num"]
            df['file_name'] = splitted_page_text["file_name"]
            df['id'] = df.apply(lambda x : str(uuid.uuid4()), axis=1)
            splitted_text_df = pd.concat([splitted_text_df, df], ignore_index=True)
        splitted_text_df["page_num"] = splitted_text_df["page_num"].astype(str)    

        # split df to 50 records per batch
        # df_array = np.array_split(df, len(df) // 50 + 1)  
        # data_array_count = len(df_array)

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