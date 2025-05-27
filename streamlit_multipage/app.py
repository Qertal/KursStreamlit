import streamlit as st

def home_page():
    st.title("Home")


def about_page():
    st.title("About")


def help_page():
    st.title("Help")

#streamlit page
home = st.Page(home_page, title="Home",icon=":material/home:")
about = st.Page(about_page, title="About",icon=":material/settings:")
help = st.Page(help_page, title="Help",icon=":material/help:")

info = st.Page("pages/info_page.py", title="Info",icon=":material/info:")

#navigation
# #without sections
# pg = st.navigation([home, about, help, info])

#without sections
pg = st.navigation({
    "Home":[home],
    "About": [help,about,info]
    })

#page link
st.page_link("https://streamlit.io/", label="Streamlit official")
st.page_link("pages/info_page.py", label="Info")


pg.run()