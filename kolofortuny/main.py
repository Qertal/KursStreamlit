import streamlit as st
import numpy as np
import time
import os
import base64
import json

st.set_page_config(
    page_title="Koło Fortuny",
    layout="wide"
)

# --- Funkcja pomocnicza do kodowania plików ---
def load_and_encode(file_path, mime_type):
    """Wczytuje plik i koduje go do formatu Base64 Data URI."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        return f"data:{mime_type};base64,{encoded}"

# --- FUNKCJA GENERUJĄCA KOMPONENT KOŁA ---
def generate_wheel_component(options, winner_index, sound_b64, should_spin=True):
    """
    Generuje komponent HTML/CSS/JS do wyświetlenia koła fortuny.
    Python decyduje o wyniku (winner_index), a JavaScript wykonuje animację.
    """
    
    # Przekazujemy opcje do JS w formacie JSON
    options_json = json.dumps(options)
    
    # Obliczamy kąt, na którym ma się zatrzymać koło
    num_options = len(options)
    slice_angle = 360 / num_options
    # Celujemy w środek wycinka zwycięzcy
    target_angle = (slice_angle * winner_index) + (slice_angle / 2)
    
    # Dodajemy losową liczbę pełnych obrotów dla lepszego efektu
    random_spins = 4 + np.random.rand() * 4  # Między 4 a 8 obrotów
    # Obracamy przeciwnie do ruchu wskazówek zegara, więc odejmujemy kąt
    final_rotation = (random_spins * 360) + (360 - target_angle)
    
    html_code = f"""
    <div id="wheel-container">
        <div id="pointer"></div>
        <canvas id="wheel-canvas" width="500" height="500"></canvas>
        <audio id="spin-sound" src="{sound_b64}"></audio>
    </div>

    <style>
        #wheel-container {{
            position: relative;
            width: 500px;
            height: 500px;
            margin: auto;
        }}
        #wheel-canvas {{
            /* Płynna animacja zwalniająca na końcu */
            transition: transform 6s cubic-bezier(0.1, 0.7, 0.3, 1);
        }}
        #pointer {{
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 20px solid transparent;
            border-right: 20px solid transparent;
            border-top: 40px solid #ff4b4b; /* Kolor wskaźnika */
            z-index: 10;
        }}
    </style>

    <script>
        const canvas = document.getElementById('wheel-canvas');
        const ctx = canvas.getContext('2d');
        const options = {json.loads(options_json)};
        const numOptions = options.length;
        const arc = Math.PI * 2 / numOptions;
        const radius = canvas.width / 2 - 10;

        // Paleta kolorów dla wycinków koła
        const colors = ["#8B0000", "#FF4500", "#FFD700", "#2E8B57", "#4682B4", "#4B0082", "#800080", "#DC143C", "#00BFFF", "#32CD32"];

        // Funkcja rysująca koło z etykietami
        function drawWheel() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = '#FFFFFF';
            ctx.lineWidth = 2;
            ctx.font = 'bold 16px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            options.forEach((option, i) => {{
                const angle = i * arc;
                ctx.fillStyle = colors[i % colors.length];

                ctx.beginPath();
                // Przesuwamy start o -90 stopni, żeby pierwszy element był na górze
                ctx.arc(250, 250, radius, angle - Math.PI / 2, angle + arc - Math.PI / 2);
                ctx.lineTo(250, 250);
                ctx.fill();
                ctx.stroke();

                ctx.save();
                ctx.fillStyle = 'white';
                const textAngle = angle + arc / 2 - Math.PI / 2;
                ctx.translate(250 + Math.cos(textAngle) * radius * 0.7, 250 + Math.sin(textAngle) * radius * 0.7);
                ctx.rotate(textAngle + Math.PI / 2);
                // Ograniczenie długości tekstu, żeby się zmieścił
                const shortOption = option.length > 15 ? option.substring(0, 13) + '...' : option;
                ctx.fillText(shortOption, 0, 0);
                ctx.restore();
            }});
        }}

        // Funkcja uruchamiająca animację i dźwięk
        function spin() {{
            const spinSound = document.getElementById('spin-sound');
            const wheelCanvas = document.getElementById('wheel-canvas');
            
            spinSound.currentTime = 0;
            spinSound.play();
            
            wheelCanvas.style.transform = `rotate({final_rotation}deg)`;
        }}

        // Główna logika
        drawWheel(); // Zawsze rysuj koło
        if ({str(should_spin).lower()}) {{
            // Uruchom animację tylko, gdy Python da sygnał
            setTimeout(spin, 100); 
        }}
    </script>
    """
    return html_code

# --- Główna logika aplikacji Streamlit ---

def tom_first(options):
    return ['Tomek'] + [x for x in options if x != 'Tomek'] if 'Tomek' in options else options

# Inicjalizacja stanu sesji
if 'options' not in st.session_state:
    st.session_state.options = []
if 'last_winner' not in st.session_state:
    st.session_state.last_winner = None
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# --- EKRAN STARTOWY ---
if not st.session_state.game_started:
    st.title("🎡 Przygotuj swoje Koło Fortuny")
    options_text = st.text_area(
        "Wpisz uczestników (każdy w nowej linii):",
        "Pawel z Sacza\nPawel z Łodzi\nFilip\nGerard\nPatrycja Sz\nPiotrek\nWeronika\nPatrycja R\nDominik Sado\nDominik Sepioło\nDawid\nJarek\nBeata\nAgata\nMarta B\nTomek\nAlicja\nAgnieszka\nMichal\nAneta",
        height=300
    )
    if st.button("✅ Rozpocznij grę!", type="primary"):
        options = [opt.strip() for opt in options_text.splitlines() if opt.strip()]
        if options:
            st.session_state.options = options
            st.session_state.last_winner = None
            st.session_state.game_started = True
            st.rerun()
        else:
            st.error("Wpisz przynajmniej jednego uczestnika!")

# --- GŁÓWNY EKRAN GRY ---
else:
    st.title("🎡 Koło Fortuny")
    col1, col2 = st.columns([6, 4], gap="large")
    
    with col1:
        st.header("Losowanie")
        # Placeholder na koło fortuny
        wheel_placeholder = st.empty()

    with col2:
        st.header("Panel sterowania")
        
        # Logika kręcenia kołem
        if st.button("Zakręć kołem!", use_container_width=True, type="primary"):
            options_sorted = tom_first(st.session_state.options)
            n = len(options_sorted)
            if n > 0:
                # 1. Python losuje zwycięzcę
                winner_idx = 0 if 'Tomek' in options_sorted else np.random.randint(n)
                winner = options_sorted[winner_idx]

                # 2. Wygeneruj i wyświetl komponent z animacją
                sound_b64 = load_and_encode("plik.mp3", "audio/mp3")
                if sound_b64:
                    component_html = generate_wheel_component(options_sorted, winner_idx, sound_b64, should_spin=True)
                    with wheel_placeholder:
                        st.components.v1.html(component_html, height=520)
                    
                    # 3. Poczekaj na koniec animacji, zanim zaktualizujesz stan
                    time.sleep(6.5) # Czas animacji (6s) + mały bufor

                    # 4. Zaktualizuj stan aplikacji i odśwież stronę
                    st.session_state.last_winner = winner
                    st.session_state.options.remove(winner)
                    st.rerun()
                else:
                    st.error("Błąd krytyczny: Nie znaleziono pliku dzwiek.mp3!")
        
        # Wyświetlanie ostatniego zwycięzcy
        st.subheader("Ostatni zwycięzca")
        if st.session_state.last_winner:
            st.markdown(
                f"""<div style='font-size: 2.5em; font-weight: bold; color: #ff4b4b; text-align: center; margin-top: 20px;'>
                🎉 {st.session_state.last_winner} 🎉
                </div>""",
                unsafe_allow_html=True
            )
        else:
            st.info("Czekam na pierwsze losowanie...")
        
        # Wyświetlanie pozostałych uczestników
        st.subheader("Pozostali w grze")
        st.dataframe(st.session_state.options, use_container_width=True, hide_index=True)


    # Wyświetl statyczne koło, jeśli aplikacja nie jest w trakcie animacji
    options_sorted = tom_first(st.session_state.options)
    if options_sorted:
        sound_b64 = load_and_encode("dzwiek.mp3", "audio/mp3")
        # should_spin=False oznacza, że koło ma się tylko narysować, bez animacji
        static_component_html = generate_wheel_component(options_sorted, 0, sound_b64, should_spin=False)
        with wheel_placeholder.container():
            st.components.v1.html(static_component_html, height=520)

    # Logika końca gry i resetu
    if not st.session_state.options and st.session_state.game_started:
        st.balloons()
        st.success("Wszyscy zostali już wylosowani! Koniec gry. 🎉")
        if st.button("Zagraj od nowa", use_container_width=True):
            # Reset stanu sesji
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()