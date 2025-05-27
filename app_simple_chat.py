import streamlit as st

#create a storage for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#display previous chat history

# st.write(st.session_state.messages)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message['content'])

prompt = st.chat_input("Ask Something")
if prompt:
    #display the message

    #add the user prompt to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # with st.chat_message("assistant"):
    #     st.write(prompt)

    # #custom

    # with st.chat_message("bot",avatar='😀'):
    #     st.write(prompt)

#display 