#Basics and fundamentals

#core packages
import streamlit as st

# working with widgets
# buttons/radio/checkbox/select/

# workign with buttons
name = "Jesse"

if st.button("Submit"):
    st.write(f"Name: {name.upper()}")

if st.button("Submit", key = 'new02'):
    st.write(f"First Name: {name.lower()}")    

#Working with radiobuttons

status = st.radio("What is your status?", ("Active","Incactive"))

if status == "Active":
    st.success("You are active!")
elif status == "Incactive":
    st.warning("Inactive")

#Working with checkbox

if st.checkbox("Show/Hide"):
    st.text("Showing something")

#working with beta expander

with st.expander("Python"):
    st.success("Twój kod lub treść tutaj")

with st.expander("Julia"):
    st.text("Hello Julia")