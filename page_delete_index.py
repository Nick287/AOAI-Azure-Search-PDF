import streamlit as st
import pandas as pd
import numpy as np
from function.AzureVectorSearch import AzureVectorSearch
from function.ChromaHelper import ChromaHelper


st.title('Index Management')
st.subheader('Delete Index')

# azureVectorSearch = AzureVectorSearch()
chromaHelper = ChromaHelper()

if 'rerun' not in st.session_state:
    st.session_state['rerun'] = False

with st.spinner(text="Loading..."):
    # index_names = azureVectorSearch.list_index_names()
    index_names = chromaHelper.list_index_names()
    selected_index_name = st.selectbox('Please select an index name.',index_names)

if st.button('Delete Index'):
    if selected_index_name == None:
        st.stop()
    else:
        with st.spinner('Deleting index...'):
            if st.session_state.rerun:
                st.session_state.rerun = False
                st.stop()
                pass

            # azureVectorSearch.delete_search_index(selected_index_name)
            chromaHelper.delete_index(selected_index_name)
            st.session_state['rerun'] = True
            st.rerun()