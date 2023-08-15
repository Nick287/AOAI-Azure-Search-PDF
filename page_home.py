import streamlit as st
from st_pages import Page, show_pages, add_page_title

# Streamlit application
def main():
    add_page_title()
    show_pages(
        [
            Page("page_create_index.py", "Create Index", "✏️", True),
            Page("page_delete_index.py", "Delete Index", "🎈"),
            Page("page_upload_data.py", "Upload Data", ":books:"),
            Page("page_vector_search.py", "Vector Search", "🎉"),
        ]
    )

if __name__ == "__main__":
    main()