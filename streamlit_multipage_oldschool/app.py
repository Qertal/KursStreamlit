import streamlit as st

my_variable = "From Main App.py Page"

def main():
    st.subheader("Main Page")
    st.title("Streamlit Multi-Page")
    st.write(my_variable)

    choice = st.sidebar.selectbox("Submenu",['Pandas','Tensforflow'])
    if choice == "Pandas":
        st.subheader("Pandas")

if __name__ == '__main__':
    main()