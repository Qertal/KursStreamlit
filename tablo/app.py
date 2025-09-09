import streamlit as st
import os

st.set_page_config(layout="wide")

def home_page():
    st.title("Tablo zdrajców")

    st.subheader("Z panelu z lewej strony wybierz, do którego tablo chcesz przejść.")
    st.markdown("""
                Implementacja autorstwa:
                **Pawła Drzyzgi**.
                """)
    

home = st.Page(home_page, title = 'Tablo', icon='🏠')

zdrajcow = st.Page("pages/zdrajcow.py", title='Zdrajców')
zdradzonych = st.Page("pages/zdradzonych.py", title="Zdradzonych")

pg = st.navigation(
    {
        "Strona główna": [home],
        "Tablo": [zdrajcow, zdradzonych]
    }
)

pg.run()