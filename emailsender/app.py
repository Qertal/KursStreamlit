import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os

st.title("🎥 Kompresja małego filmu")

uploaded_file = st.file_uploader("Wgraj plik MP4 (do 50 MB)", type=["mp4"])

if uploaded_file is not None:
    # Zapisujemy oryginał do pliku tymczasowego
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(uploaded_file.read())
        temp_input_path = temp_input.name

    st.video(temp_input_path)

    st.info("🔄 Trwa kompresja...")

    # Kompresujemy film do mniejszej rozdzielczości i bitrate
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output:
            clip = VideoFileClip(temp_input_path)
            # Przytnij jakość i rozdzielczość do np. 480p
            clip_resized = clip.resize(height=480)  # lub width=640
            clip_resized.write_videofile(
                temp_output.name,
                codec="libx264", 
                bitrate="500k",   # można ustawić 200k dla mniejszego rozmiaru
                audio_codec="aac"
            )
            output_path = temp_output.name

        st.success("✅ Kompresja zakończona!")
        with open(output_path, "rb") as f:
            st.download_button("Pobierz skompresowany film", f.read(), file_name="compressed.mp4")

        # Sprzątanie
        clip.close()
        os.remove(temp_input_path)
        os.remove(output_path)

    except Exception as e:
        st.error(f"Błąd podczas kompresji: {str(e)}")
