import streamlit as st
import numpy as np
from pages.func import kula

st.set_page_config(page_title="Rysowanie kuli na płaszczyźnie", layout="wide")
st.title("Rysowanie kuli na płaszczyźnie")


col1, col2 = st.columns(2)
with col1:
    with st.form("form"):
        typ = st.selectbox("Wybierz typ kuli:", ['domknieta', 'otwarta', 'sfera'])
        srodek_x = st.number_input("Współrzędna x środka kuli:", value=0, step=1)
        srodek_y = st.number_input("Współrzędna y środka kuli:", value=0, step=1)
        promien = st.number_input("Promień kuli:", value=2., min_value=1.5, max_value = 10., step=.1)
        metryka = st.number_input("Metryka (p):", value=2.0, min_value=0.2 ,max_value=75.0, step=0.1)

        submitted = st.form_submit_button("Rysuj")

if submitted:
    with col2:
        kula(typ, metryka, srodek_x, srodek_y, promien)

