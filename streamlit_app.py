import streamlit as st
from time import sleep
from navigation import make_sidebar

make_sidebar()

st.title("Welcome to RAG Chat Bot")

st.write("Please log in to continue (username `*****`, password `*****`).")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Log in", type="primary"):
    if username == "admin" and password == "admin123456":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        st.switch_page("pages/page_create_index.py")
    else:
        st.error("Incorrect username or password")