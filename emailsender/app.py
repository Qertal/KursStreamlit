import streamlit as st
import ffmpeg
import tempfile
import os

st.title("Kompresja wideo")

uploaded_file = st.file_uploader("Wgraj film", type=["mp4"])

if uploaded_file is not None:
    st.video(uploaded_file)  # pokazuje podgląd
    with open("temp.mp4", "wb") as f:
        f.write(uploaded_file.read())  # zapisuje na dysk

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input:
        tmp_input.write(uploaded_file.read())
        input_path = tmp_input.name

    output_path = input_path.replace(".mp4", "_compressed.mp4")

    st.info("Kompresuję wideo...")

    ffmpeg.input(input_path).output(output_path, vcodec='libx264', crf=28).run()

    with open(output_path, "rb") as file:
        st.download_button("Pobierz skompresowany plik", file.read(), file_name="compressed.mp4")

    # Sprzątanie
    os.remove(input_path)
    os.remove(output_path)
