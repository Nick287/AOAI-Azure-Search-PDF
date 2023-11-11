import streamlit as st
from st_pages import Page, show_pages, add_page_title
from function.AzureAIToken import *
from app_config.keys_config import *

def check_password():
    # """Returns `True` if the user had a correct password."""

    def password_entered():        
        # """Checks whether a password entered by the user is correct."""
        if (
            # st.session_state["username"] in st.secrets["passwords"]
            # and st.session_state["password"]
            # == st.secrets["passwords"][st.session_state["username"]]

            # hardcode username and password here just for testing purpose, please remove it in production
            st.session_state["username001"] == "admin" and
            st.session_state["password001"] == "admin123456"
        ):
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
            return True
        else:
            return False

    st.title("Log In")
    st.session_state["username001"] = st.text_input("Username", key="username")
    st.session_state["password001"] = st.text_input("Password", type="password", key="password")
    if st.button("Login"):
        if password_entered():
            st.session_state.password_correct = True
            st.experimental_rerun()
        else:
            st.error("😕 wrong username or password")

def init():
    add_page_title()
    show_pages(
        [
            Page("page_create_index.py", "Create Index", "✏️", True),
            Page("page_delete_index.py", "Delete Index", "🎈"),
            Page("page_upload_data.py", "Upload Data", ":books:"),
            Page("page_vector_search.py", "Vector Search", "🎉"),
        ]
    )

# Streamlit application
def main():
    if Login == "True":
        if "password_correct" not in st.session_state:
            st.session_state.password_correct = False
        if not st.session_state["password_correct"]:
            check_password()
        else:
            init()
    else:
        init()

if __name__ == "__main__":
    main()