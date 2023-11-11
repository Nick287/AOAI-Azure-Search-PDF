import streamlit as st
import pandas as pd
import numpy as np

from function.vectory_db_helper.vectory_db_factory import *
from function.abstract_vectory_db.vectory_db import *

vectory_db = vectory_db_factory().create_vectory_db(vectory_db_type.azure_cognitive_search)

st.title('Index Management')
st.subheader('Delete Index')

with st.spinner(text="Loading..."):
    index_names = vectory_db.list_index_names()
    st.session_state.item = None
    selected_index_name = st.selectbox('Please select an index name.',index_names,index=st.session_state.item)

if st.button('Delete Index'):
    if selected_index_name == None:
        st.stop()
    else:
        with st.spinner('Deleting index...'):
            # azureVectorSearch.delete_search_index(selected_index_name)
            vectory_db.delete_index(selected_index_name)
            st.session_state.item = None
            st.rerun()