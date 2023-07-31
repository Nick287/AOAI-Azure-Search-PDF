import streamlit as st
from io import BytesIO 
import pandas as pd
import numpy as np

from function.NormalizeText import NormalizeText
from function.LangChainChunking import LangChanSplitter
from function.AzureVectorSearch import AzureVectorSearch


st.title('Upload PDF file for Azure Vector Search')

with st.spinner(text="Loading..."):
    azureVectorSearch = AzureVectorSearch()
    index_names = azureVectorSearch.list_index_names()
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

        content_pd = pd.DataFrame({'content': stirnglist})
        df = content_pd.reset_index()
        df = df.rename(columns={'index': 'id'})

        # split df to 50 records per batch
        df_array = np.array_split(df, len(df) // 50 + 1)  
        data_array_count = len(df_array)
        # create search index
        azureVectorSearch = AzureVectorSearch()
        azureVectorSearch.create_search_index(index_name)
        with st.expander(f"log info:"):
            st.info("total batch job: " + str(data_array_count))
            new_df_array = []
            current_job_numeber = 1
            for sub_df in df_array:
                st.info("working on: " + str(current_job_numeber) + "/" +str(data_array_count))
                sub_df['id'] = sub_df["id"].apply(lambda x : str(x + 1))
                sub_df['product'] = sub_df["id"].apply(lambda x : "you can customise this field")
                sub_df['category'] = sub_df["id"].apply(lambda x : "you can customise this field")
                sub_df['contentVector'] = sub_df["content"].apply(lambda x : azureVectorSearch.generate_embeddings(x))
                # upload data
                list_of_dict = sub_df.to_dict('records')  
                azureVectorSearch.upload_documents(index_name,list_of_dict)
                new_df_array.append(sub_df)
                current_job_numeber+=1

            new_df = pd.concat(new_df_array, axis=0, ignore_index=True) 
            st.info(str(len(new_df)) + " records uploaded.")
    st.success("done!")