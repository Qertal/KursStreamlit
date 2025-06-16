import streamlit as st

st.set_page_config(page_title="Odtwarzacz wideo", layout="centered")

st.title("🎬 Odtwarzacz wideo")

uploaded_file = st.file_uploader("Wgraj plik wideo", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    st.success(f"Plik „{uploaded_file.name}” został wgrany.")
    st.video(uploaded_file)
