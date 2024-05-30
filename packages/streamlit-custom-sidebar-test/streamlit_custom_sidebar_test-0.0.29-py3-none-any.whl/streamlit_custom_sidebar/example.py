import streamlit as st

st.set_page_config(layout="wide")

from slim_expand_sidebar.__init__ import NoHoverExpandSidebarTemplate, HoverExpandSidebarTemplate

# st.set_page_config()

current_page = "example"


data_ = [
            {"index":0, "label":"Example", "page_name":"example", "page_name_programmed":"example.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/"},
            {"index":1, "label":"Page", "page_name":"page", "page_name_programmed":"pages/page.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
        ]

base_data_ = [
    {"index":0, "label":"Settings", "page_name":"settings", "page_name_programmed":"None", "icon":"settings", "iconLib":"Google"},
    {"index":1, "label":"Logout", "page_name":"logout", "page_name_programmed":"None", "icon":"ri-logout-box-r-line", "iconLib":""}
]

test_sidebar_ = NoHoverExpandSidebarTemplate(closedOnLoad=False, base_data=base_data_, data=data_, logoUrl="https://www.google.co.uk", logoText="Optum Gamer", logoTextSize="20px")
test_sidebar_.load_custom_sidebar()
# active_navigation()

st.write("**Sup Bro**")
# st.write("**Hey Man, Bro**")

