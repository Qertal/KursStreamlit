import streamlit as st
import ffmpeg
import os
import tempfile

# --- Konfiguracja strony ---
st.set_page_config(
    page_title="Kompresor Wideo",
    page_icon="🎬",
    layout="wide"
)

# --- Poprawiona funkcja kompresująca ---
def compress_video(input_path: str, output_path: str, crf: int, resolution: str):
    """
    Kompresuje plik wideo z zadanymi parametrami.
    """
    try:
        # Zawsze zaczynaj od strumienia wejściowego
        stream = ffmpeg.input(input_path)

        # Zbuduj słownik z argumentami dla wyjścia
        output_args = {
            'vcodec': 'libx264',
            'crf': crf,
            'preset': 'medium'
        }

        # Jeśli wybrano zmianę rozdzielczości, DODAJ filtr do słownika argumentów
        if resolution != "Oryginalna":
            height = int(resolution.replace('p', ''))
            output_args['vf'] = f'scale=-1:{height}' # vf to filtr wideo (video filter)

        # Wywołaj .output() TYLKO RAZ na końcu, przekazując wszystkie argumenty
        stream = ffmpeg.output(stream, output_path, **output_args)
        
        # Uruchomienie kompresji
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        return True, None
        
    except ffmpeg.Error as e:
        error_message = e.stderr.decode()
        return False, error_message

# --- Interfejs aplikacji ---
st.title("🎬 Interaktywny Kompresor Wideo")
st.markdown("""
Witamy w aplikacji do kompresji wideo! Ta aplikacja używa potężnego narzędzia **FFmpeg** w tle.
1.  **Prześlij** swój plik wideo.
2.  **Ustaw** parametry kompresji w panelu bocznym.
3.  **Kliknij** przycisk "Kompresuj wideo".
4.  **Porównaj** jakość i rozmiar, a następnie **pobierz** wynik!
""")

# --- Panel boczny z ustawieniami ---
with st.sidebar:
    st.header("⚙️ Ustawienia Kompresji")
    
    selected_crf = st.slider(
        "Wybierz jakość (CRF)",
        min_value=18, max_value=35, value=28,
        help="Niższa wartość = lepsza jakość, większy plik. Wyższa wartość = gorsza jakość, mniejszy plik. Wartość 23-28 to dobry kompromis."
    )

    selected_resolution = st.selectbox(
        "Wybierz docelową rozdzielczość (wysokość)",
        options=["Oryginalna", "1080p", "720p", "480p", "360p"],
        index=2,
        help="Zmiana rozdzielczości znacząco wpływa na rozmiar pliku."
    )

# --- Główny obszar aplikacji ---
uploaded_file = st.file_uploader("1. Prześlij plik wideo", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tfile:
        tfile.write(uploaded_file.read())
        input_video_path = tfile.name

    st.subheader("Oryginalne wideo")
    st.video(input_video_path)

    if st.button("🚀 Kompresuj wideo!", use_container_width=True):
        output_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

        with st.spinner(f"Trwa kompresja... To może potrwać kilka minut w zależności od rozmiaru pliku i wybranych ustawień."):
            success, error_details = compress_video(input_video_path, output_video_path, selected_crf, selected_resolution)

        if success:
            st.success("✅ Kompresja zakończona sukcesem!")

            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Przed kompresją")
                st.video(input_video_path)
                original_size = os.path.getsize(input_video_path) / (1024 * 1024)
                st.metric("Rozmiar pliku", f"{original_size:.2f} MB")

            with col2:
                st.subheader("Po kompresji")
                st.video(output_video_path)
                compressed_size = os.path.getsize(output_video_path) / (1024 * 1024)
                st.metric("Rozmiar pliku", f"{compressed_size:.2f} MB")

            gain = 100 * (1 - compressed_size / original_size) if original_size > 0 else 0
            st.metric("📉 Zysk miejsca", f"{gain:.2f}%")

            with open(output_video_path, "rb") as file:
                st.download_button(
                    label="📥 Pobierz skompresowane wideo",
                    data=file,
                    file_name=f"skompresowany_{uploaded_file.name}",
                    mime="video/mp4",
                    use_container_width=True
                )
            
            os.remove(input_video_path)
            os.remove(output_video_path)

        else:
            st.error("❌ Wystąpił błąd podczas kompresji.")
            st.code(error_details, language="bash")
            os.remove(input_video_path)