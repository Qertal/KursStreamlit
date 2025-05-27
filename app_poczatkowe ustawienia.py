#Core packages
import streamlit as st
from PIL import Image
img = Image.open('Facebook_logo.png')
# Must be the first activity of streamlit


# Method 1
# st.set_page_config(page_title='Hello world',
#                    page_icon=img,
#                    layout='wide',
#                    initial_sidebar_state="collapsed")



#Method 2: Dictionary
PAGE_CONFIG = {
    "page_title": "Stronka",
    "page_icon": img,
    "layout": "centered",
    "initial_sidebar_state": "auto"
}
st.set_page_config(**PAGE_CONFIG)

#Additionak packages

#Fxns

def main():
    """
    All your code goes here
    """
    st.title("Hello Streamlit lovers")
    st.sidebar.success("Hello")

if __name__ == '__main__':
    main()