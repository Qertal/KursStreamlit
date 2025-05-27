import streamlit as st

from eda_app import run_eda_app

from ml_app import run_ml_app

#utils

import logging

# TERMINAL
# # FORMAT
# LOGS_FORMAT = "%(levelname)s %(asctime)s.%(msecs)03d - %(message)s"
# DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# # Create a logger
# logging.basicConfig(level=logging.DEBUG, format=LOGS_FORMAT, datefmt=DATE_FORMAT)
# logger = logging.getLogger(__name__)

#SAVE to file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

#Formatter
formatter = logging.Formatter("%(levelname)s %(asctime)s.%(msecs)03d - %(message)s")
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

#file

file_handler = logging.FileHandler('activity.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def main():
    st.title("Main app")
    st.title("Adding logs to app")
    st.text("Track all activities on app")

    menu = ['Home','EDA','ML','About']
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        logger.info("Home Section")


    elif choice == 'EDA':
        run_eda_app()
        logger.info("EDA Section")
    elif choice == 'ML':
        run_ml_app()
        logger.info("ML Section")
    else:
        st.subheader("Abouts")
        logger.info("About Section")    


if __name__ == '__main__':
    main()