import streamlit as st
import os

files = os.listdir(os.getcwd() + '/tablo/zdradzonych/')

members = {}
for i in files:
    member = os.path.splitext(i)[0].split('_')
    members[member[0]] = member[1], i, int(member[0])%3

col0, col1, col2 = st.columns([3,3,3])

with col1:
    st.title('Tablo zdradzonych')

for id, (name, filename, column) in members.items():
    # st.image('zdrajcow/' + filename, caption=name)
    if column == 0:
        col0, col1, col2 = st.columns(3)
    if column == 0:
        with col0:
            st.image('tablo/zdradzonych/' + filename, caption=name, use_container_width=True)
    elif column == 1:
        with col1:
            st.image('tablo/zdradzonych/' + filename, caption=name, use_container_width=True)
    else:
        with col2:
            st.image('tablo/zdradzonych/' + filename, caption=name, use_container_width=True)