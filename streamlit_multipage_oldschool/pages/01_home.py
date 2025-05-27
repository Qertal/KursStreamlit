import streamlit as st

#sharing variables among pages
from app import my_variable

#from pages.02_eda import my_calc

st.subheader("Home Page")
st.write(my_variable)
#st.write(my_calc)