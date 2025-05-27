#Basics and fundamentals

#core packages
import streamlit as st

# laod eda pkgs
import pandas as pd

# Display data

df = pd.read_csv('iris.csv')

# Method 1
st.dataframe(df, width= 200,height = 100)

# Add a color style from pandas
st.dataframe(df.style.highlight_max(axis=0))


# Method 2: Static table

st.table(df)

# Method 3: Using superfunction st.write

st.write(df.head())

#Displaying Json

st.json({'data': "name"})

#Display Code
mycode = """
def sayhellow():
    print("Hello streamlit lovers")
"""
st.code(mycode, language='python')