#Core packages
import streamlit as st

#Additionak packages

#Fxns

def main():
    """
    All your code goes here
    """
    st.title("Hello Streamlit lovers")

if __name__ == '__main__':
    main()

# Text

liczba = 54

st.text('Hello world')
st.text(f'Witam {liczba}')

# Header

st.header("This is header")

# Subheader

st.subheader("This is subheader")

# Title

st.title("This is title")

# Markdown

st.markdown("## This is markdown")

# Displaying Colored Text/Boostraps Alert

st.success('Succesful')
st.warning('Warning')
st.info('Info')
st.error('Error')
st.exception('Exception')

# Superfunction
st.write('Normal text')
st.write('## This is a text')
st.write(1+2)

st.write(dir(st))

# Help info
st.help(range)