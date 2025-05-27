import streamlit as st

#text input

fname = st.text_input("Enter Firstname", max_chars=10)
st.title(fname)

#text area

message = st.text_area("Enter message", height=70)
st.write(message)


#numbers

number = st.number_input("Enter number",min_value= 1., max_value= 10., step = 0.01)

#date input

myappointment = st.date_input("Appointemnt")

#time input

mytime = st.time_input("My Time")

#tixt input hide password

password = st.text_input("Enter password", type="password")

# color picker

color = st.color_picker("Select color")

# message input
message = st.chat_input("Message")