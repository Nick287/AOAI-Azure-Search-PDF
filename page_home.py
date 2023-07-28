from st_pages import Page, show_pages, add_page_title
import streamlit as st

# Optional -- adds the title and icon to the current page
# add_page_title()


# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("page_create_index.py", "Create Index", "✏️"),
        Page("page_delete_index.py", "Delete Index", "🎈"),
        Page("page_upload_data.py", "Upload Data", ":books:"),
        Page("page_vector_search.py", "Vector Search", "🎉"),
    ]
)