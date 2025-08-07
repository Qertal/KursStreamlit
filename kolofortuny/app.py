import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random

st.set_page_config(
    page_title="Koło Fortuny",
    layout="wide")

def tom_first(options):
    # Jeśli "Tomek" jest w liście, umieść go na początku, a resztę przetasuj
    if 'Tomek' in options:
        others = [x for x in options if x != 'Tomek']
        random.shuffle(others)
        return ['Tomek'] + others
    else:
        random.shuffle(options)
        return options

if 'options' not in st.session_state:
    st.session_state.options = []
if 'last_winner' not in st.session_state:
    st.session_state.last_winner = None

# Wpisywanie opcji tylko na początku gry
if not st.session_state.options:
    options = st.text_area(
        "Wpisz opcje (każda w nowej linii):",
        """Pawel z Sacza
Pawel z Łodzi
Filip
Gerard
Patrycja Sz
Piotrek
Weronika
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
Agnieszka
Michal
Aneta"""
    ).splitlines()

    if st.button("Zatwierdź opcje") and len([opt for opt in options if opt.strip()]):
        st.session_state.options = [opt for opt in options if opt.strip()]
        st.session_state.last_winner = None

if st.session_state.options:
    col4, col1, col2, col3 = st.columns([1,5,5,1])  # poidzial na kolsy, zeby to w miare sensownie wygladalo
    with col1:
        spin = st.button("Zakręć kołem!")
        if 'spinning' not in st.session_state:
            st.session_state.spinning = False

        options_sorted = tom_first(st.session_state.options)
        n = len(options_sorted)

        if spin and not st.session_state.spinning:
            st.session_state.spinning = True
            spin_placeholder = st.empty()
            # tomek pierwszy, do dodania siebie gdzies chociaz w miare na poczatku XD, coś a'la 3/4, ewentualnie pod koniec jak i tak losuje
            if 'Tomek' in options_sorted:
                winner_idx = 0
            else:
                winner_idx = np.random.randint(n)

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
                time.sleep(0.05 + 0.005 * i)
            st.session_state.spinning = False
            winner = options_sorted[winner_idx]
            st.session_state.last_winner = winner
            st.session_state.options.remove(winner)
            time.sleep(1.0)
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
        else:
            st.info("Czekam na losowanie...")

    # Reset po skończeniu gry
    if not st.session_state.options:
        st.info("Wszystkie opcje zostały już wylosowane! 🎉")
        if st.button("Zagraj od nowa"):
            del st.session_state.options
            st.session_state.last_winner = None
else:
    st.info("Wpisz opcje i zatwierdź, aby rozpocząć zabawę!")
