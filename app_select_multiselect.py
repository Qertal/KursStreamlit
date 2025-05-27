import streamlit as st

#select/multiselect 

my_lang = ['Python','Julia','Go','Rust']

choice = st.selectbox("Language", my_lang)

st.write(f"You selected {choice}")

#multiple

spoken_lang = ('English','French','Spanish','Twi')

my_spoken_pang = st.multiselect("Spoken Lang",spoken_lang, default='English')

#slider
#numbers (int /float /dates)
age = st.slider("wartosc wspolrzednej",1,100000000, value = (2,1000))
ega = st.slider("wartosc wspolrzednejj",1,100000000, value = (2))

#any datatype
#select slider

color = st.select_slider('Choose color', options=['yellow','red','blue','black','green'], value=('yellow','red'))

