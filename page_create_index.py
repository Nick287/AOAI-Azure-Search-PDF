import streamlit as st
from function.vectory_db_helper.vectory_db_factory import *
from function.abstract_vectory_db.vectory_db import *
from app_config.keys_config import *
from app_config.website_config import *

vectory_db = vectory_db_factory().create_vectory_db(DB_TYPE)

st.title('Index Management')
st.subheader('Create Index')
index_name = st.text_input('Please input index name')

if st.button('Create Index') or index_name != '':
    if index_name == '':
        st.error('Please input index name!')
        st.stop()
    else:
        with st.spinner('Creating index...'):
            # azureVectorSearch.create_search_index(index_name)
            vectory_db.create_index(index_name)
            st.success("done!")