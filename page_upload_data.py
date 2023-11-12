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

vectory_db = vectory_db_factory().create_vectory_db(DB_TYPE)

st.title('Upload PDF file to Vector DB for Search')

with st.spinner(text="Loading..."):
    index_names = vectory_db.list_index_names()
    index_name = st.selectbox('Please select an index name.',index_names)
    st.write('You selected:', index_name)

uploaded_file = st.file_uploader("Please Choose a DPF file",type="pdf")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    pdf_file = BytesIO(bytes_data) 

    with st.spinner(text="Document uploading..."):
        # read pdf file
        pdf_reader = NormalizeText()
        longtxt = pdf_reader.get_doc_content_txt(pdf_file)

        pdf_reader = LangChanSplitter()
        stirnglist = pdf_reader.TokenTextSplitter(100,10,longtxt)

        df = pd.DataFrame({'document': stirnglist})
        df = df.dropna() 
        df['id'] = df.apply(lambda x : str(uuid.uuid4()), axis=1)  

        # split df to 50 records per batch
        df_array = np.array_split(df, len(df) // 50 + 1)  
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