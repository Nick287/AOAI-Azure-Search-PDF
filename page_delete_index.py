import streamlit as st
import pandas as pd
import numpy as np
from function.AzureVectorSearch import AzureVectorSearch
from function.ChromaHelper import ChromaHelper


st.title('Index Management')
st.subheader('Delete Index')

# azureVectorSearch = AzureVectorSearch()
chromaHelper = ChromaHelper()

with st.spinner(text="Loading..."):
    # index_names = azureVectorSearch.list_index_names()
    index_names = chromaHelper.list_index_names()
    st.session_state.item = None
    selected_index_name = st.selectbox('Please select an index name.',index_names,index=st.session_state.item)

if st.button('Delete Index'):
    if selected_index_name == None:
        st.stop()
    else:
        with st.spinner('Deleting index...'):
            # azureVectorSearch.delete_search_index(selected_index_name)
            chromaHelper.delete_index(selected_index_name)
            st.session_state.item = None
            st.rerun()