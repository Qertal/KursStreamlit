import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import os

st.set_page_config(
    page_title="Koło Fortuny",
    layout="wide")

def tom_first(options):
    # Jeśli "Tomek" jest w liście, umieść go losowo na pozycji 2., 3. lub 4.
    # Zastosujemy ważone losowanie i upewnimy się, że nie będzie pierwszy (jeśli możliwe).
    if 'Tomek' in options:
        others = [x for x in options if x != 'Tomek']
        random.shuffle(others)
        n = len(options)
        max_pos = min(3, n - 1)
        if max_pos < 1:
            # tylko Tomek
            return ['Tomek'] + others
        choices = list(range(1, max_pos + 1))
        weights = [3 if c == 1 else 2 if c == 2 else 1 for c in choices]
        pos = random.choices(choices, weights=weights, k=1)[0]
        result = others[:pos] + ['Tomek'] + others[pos:]
        # upewnij się, że Tomek nie jest pierwszy, jeśli jest inny element
        if len(result) > 1 and result[0] == 'Tomek':
            result[0], result[1] = result[1], result[0]
        return result
    else:
        random.shuffle(options)
        return options
    
def two_lucky_guys(lista: list):
    x = lista[:]
    persons = ['Pawel z Sacza','Alicja']
    possibilities = [i for i in persons if i in x]
    starting_len = len(x)
    k = 0
    while (abs(len(x) - starting_len) < 2) and k < 100:
        drop_id = random.randint(0, len(possibilities)-1)
        person_to_drop = possibilities[drop_id]
        x.remove(person_to_drop)
        possibilities.remove(person_to_drop)
        k+=1
    return x

if 'options' not in st.session_state:
    st.session_state.options = []
if 'last_winner' not in st.session_state:
    st.session_state.last_winner = None
if 'last_gif' not in st.session_state:
    st.session_state.last_gif = None
# initialize control state once
if 'spinning' not in st.session_state:
    st.session_state.spinning = False
if 'spin_attempt' not in st.session_state:
    st.session_state.spin_attempt = 0
if 'place' not in st.session_state:
    st.session_state.place = random.randint(1, 3)

# Wpisywanie opcji tylko na początku gry
if not st.session_state.options:
    options = st.text_area(
        "Wpisz opcje (każda w nowej linii):",
        """Pawel z Sacza
Pawel z Łodzi
Gerard
Patrycja Sz
Piotrek
Patrycja R
Dominik Sado
Dominik Sepioło
Dawid
Jarek
Beata
Agata
Marta B
Tomek
Alicja
Michal
Aneta
Wojciech
Wiktoria"""
    ).splitlines()

    if st.button("Zatwierdź opcje") and len([opt for opt in options if opt.strip()]):
        # options = two_lucky_guys(options)
        st.session_state.options = [opt for opt in options if opt.strip()]
        st.session_state.last_winner = None
        st.session_state.last_gif = None

if st.session_state.options:
    col4, col1, col2, col3 = st.columns([1,5,5,1])  # poidzial na kolsy, zeby to w miare sensownie wygladalo
    # use session_state counters so values persist across reruns
    iterat = st.session_state.spin_attempt
    place = st.session_state.place
    with col1:
        spin = st.button("Zakręć kołem!")
        # spinning is initialized at module start

        options_sorted = tom_first(st.session_state.options)
        n = len(options_sorted)

        if spin and not st.session_state.spinning:
            # increment attempt counter
            
            iterat = st.session_state.spin_attempt
            st.session_state.spinning = True
            spin_placeholder = st.empty()
            # tomek pierwszy, do dodania siebie gdzies chociaz w miare na poczatku XD, coś a'la 3/4, ewentualnie pod koniec jak i tak losuje
            if 'Tomek' in options_sorted and iterat == place:
                # force Tomek to win on this spin attempt
                winner_idx = options_sorted.index('Tomek')
                # after forcing, pick a new random place for next time
                st.session_state.place = random.randint(1, 3)
                st.session_state.spin_attempt = 0
                iterat = 0
            else:
                winner_idx = np.random.randint(n)
            st.session_state.spin_attempt += 1

            rounds = 1
            for i in range(rounds * n + winner_idx + 1):
                idx = i % n
                fig, ax = plt.subplots(figsize=(8, 8))
                wedges, texts = ax.pie([1]*n, labels=options_sorted, startangle=90, counterclock=False)
                for j, w in enumerate(wedges):
                    if j == idx:
                        w.set_edgecolor('red')
                        w.set_linewidth(5)
                    else:
                        w.set_edgecolor('white')
                        w.set_linewidth(1)
                ax.set_aspect('equal')
                spin_placeholder.pyplot(fig)
                plt.close(fig)
                time.sleep(0.01)
            st.session_state.spinning = False
            winner = options_sorted[winner_idx]
            st.session_state.last_winner = winner
            # wybierz losowy gif z folderu 'gifs' obok tego pliku (jeśli istnieje)
            gif_dir = os.path.join(os.path.dirname(__file__), "gifs")
            gif_list = []
            if os.path.exists(gif_dir):
                gif_list = [os.path.join(gif_dir, f) for f in os.listdir(gif_dir) if f.lower().endswith('.gif')]
            if gif_list:
                st.session_state.last_gif = random.choice(gif_list)
            else:
                st.session_state.last_gif = None

            st.session_state.options.remove(winner)
            time.sleep(0.25)
            # iterat is managed in session_state
        else:
            if options_sorted:
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.pie([1]*len(options_sorted), labels=options_sorted, startangle=90, counterclock=False)
                st.pyplot(fig)

    with col2:
        # napis ze zwyciezca
        st.markdown(
            "<div style='text-align:center;'><span style='font-size:1.8em; font-weight:bold;'>Ostatni zwycięzca:</span></div>",
            unsafe_allow_html=True
        )
        if st.session_state.last_winner:
            st.markdown(
                f"""
                <div style='
                    font-size: 3em;
                    font-weight: bold;
                    color: #ff0066;
                    text-align: center;
                    margin-top: 30px;
                    margin-bottom: 30px;
                    letter-spacing: 2px;
                    text-shadow: 2px 2px 10px #fff;
                '>
                    🎉 {st.session_state.last_winner} 🎉
                </div>
                """,
                unsafe_allow_html=True
            )
            # pokaż gif (plik .gif powinien być zapętlony samodzielnie)
            if st.session_state.last_gif:
                try:
                    # center the image in this column using inner columns
                    left, mid, right = st.columns([1, 2, 1])
                    with mid:
                        if winner == 'Tomek':
                            st.image('gifs/tomek/tomek.gif', width=540)
                        # elif winner == 'Alicja':
                            # st.image('gifs/jarek/jarek.gif', width=540)
                        else:
                            st.image(st.session_state.last_gif, width=540)
                except Exception:
                    # jeśli wyświetlenie bezpośrednie nie zadziała, pokaż informację
                    st.warning('Nie udało się wyświetlić GIF-a.')
        else:
            st.info("Czekam na losowanie...")

    # Reset po skończeniu gry
    if not st.session_state.options:
        st.info("Wszystkie opcje zostały już wylosowane! 🎉")
        if st.button("Zagraj od nowa"):
            # bezpieczny reset całego stanu gry
            st.session_state.options = []
            st.session_state.last_winner = None
            st.session_state.last_gif = None
            st.session_state.spin_attempt = 0
            st.session_state.place = random.randint(1, 3)
            st.session_state.spinning = False
else:
    st.info("Wpisz opcje i zatwierdź, aby rozpocząć zabawę!")
