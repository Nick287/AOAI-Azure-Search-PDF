import streamlit as st
import pandas as pd
import numpy as np
from function.AzureVectorSearch import AzureVectorSearch

azureVectorSearch = AzureVectorSearch()
st.title('Index Management')
st.subheader('Delete Index')

with st.spinner(text="Loading..."):
    index_names = azureVectorSearch.list_index_names()
    selected_index_name = st.selectbox('How would you like to be contacted index?',index_names)

if st.button('Delete Index'):
    if selected_index_name == '':
        st.error('Please select index name!')
        st.stop()
    else:
        with st.spinner('Deleting index...'):
            azureVectorSearch.delete_search_index(selected_index_name)
            st.success("done!")