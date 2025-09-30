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
    else:
        # nie modyfikuj oryginalnej listy w miejscu
        result = options[:]
        random.shuffle(result)

    # Nowa zasada: jeśli na liście jest "Pawel z Sacza" to przenosimy go na koniec
    if 'Pawel z Sacza' in result and len(result) > 1:
        result = [x for x in result if x != 'Pawel z Sacza'] + ['Pawel z Sacza']

    return result
    
def two_lucky_guys(lista: list):
    """Zwróć listę bez maksymalnie dwóch osób z predefiniowanej listy,
    bez ryzyka błędów przy pustych możliwościach."""
    x = lista[:]
    persons = ['Pawel z Sacza', 'Alicja']
    present = [p for p in persons if p in x]
    # wylosuj do 2 osób spośród dostępnych (jeśli są)
    to_remove = random.sample(present, k=min(2, len(present))) if present else []
    for p in to_remove:
        x.remove(p)
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
# (legacy) 'place' no longer used for Tomek forcing – can be removed safely
if 'place' in st.session_state:
    del st.session_state['place']
if 'pawel_sound' not in st.session_state:
    # flaga do wyświetlenia / odtworzenia dźwięku po wygranej Pawła
    st.session_state.pawel_sound = False

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
        # zapamiętaj liczbę początkową i ustal cel losowania dla Tomka (3 lub 4)
        st.session_state.initial_count = len(st.session_state.options)
        if 'Tomek' in st.session_state.options:
            if st.session_state.initial_count >= 4:
                # Tomek zawsze ma wypaść w 3 lub 4 losowaniu
                st.session_state.tom_target_draw = random.choice([3, 4])
            elif st.session_state.initial_count == 3:
                st.session_state.tom_target_draw = 3
            else:
                # mniej niż 3 osoby: nie da się wymusić 3/4, weź ostatni możliwy numer
                st.session_state.tom_target_draw = st.session_state.initial_count
        else:
            st.session_state.tom_target_draw = None

if st.session_state.options:
    col4, col1, col2, col3 = st.columns([1,5,5,1])  # poidzial na kolsy, zeby to w miare sensownie wygladalo
    # use session_state counters so values persist across reruns
    iterat = st.session_state.spin_attempt
    # 'place' logic removed
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
            # NOWE ZASADY LOSOWANIA XD:
            # 1) "Pawel z Sacza" zawsze ostatni (jeśli więcej niż 1 osoba na liście) pod ostatni
            # dzien przygotowowka
            # 2) "Tomek" zawsze jako 3. lub 4. (zależnie od rozmiaru listy na starcie)
            #    - przed jego docelowym numerem wykluczamy go z losowania
            #    - w jego docelowym numerze wymuszamy wygraną
            #    - jeśli z uwagi na "Pawła ostatniego" nie ma kogo losować, wybieramy Tomka
            draw_no = None
            if 'initial_count' in st.session_state and st.session_state.initial_count:
                draw_no = st.session_state.initial_count - len(st.session_state.options) + 1

            # zacznij od pełnej puli
            eligible_indices = list(range(n))
            # wyklucz Pawła, jeśli to nie ostatnia osoba
            if n > 1:
                eligible_indices = [i for i in eligible_indices if options_sorted[i] != 'Pawel z Sacza']

            forced = False
            # logika Tomka
            tom_target = st.session_state.get('tom_target_draw', None)
            if 'Tomek' in options_sorted and tom_target and draw_no:
                if draw_no == tom_target:
                    # wymuś Tomka teraz
                    winner_idx = options_sorted.index('Tomek')
                    forced = True
                elif draw_no < tom_target:
                    # wyklucz Tomka dopóki nie osiągniemy docelowego numeru
                    eligible_indices = [i for i in eligible_indices if options_sorted[i] != 'Tomek']
                    if not eligible_indices:
                        # Jeśli po wykluczeniach nie ma nikogo (zazwyczaj zostali tylko Tomek i Pawel), bierz Tomka
                        winner_idx = options_sorted.index('Tomek')
                        forced = True
                else:  # draw_no > tom_target, awaryjnie wymuś Tomka jeśli jeszcze jest
                    if 'Tomek' in options_sorted:
                        winner_idx = options_sorted.index('Tomek')
                        forced = True

            if not forced:
                if not eligible_indices:
                    eligible_indices = list(range(n))
                winner_idx = random.choice(eligible_indices)
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
            if winner == 'Pawel z Sacza':
                st.session_state.pawel_sound = True
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
                        lw = st.session_state.last_winner
                        base_dir = os.path.dirname(__file__)
                        tomek_gif = os.path.join(base_dir, 'gifs', 'tomek', 'tomek.gif')
                        pawel_gif = os.path.join(base_dir, 'gifs', 'pawel', 'pawel.gif')
                        if lw == 'Tomek' and os.path.exists(tomek_gif):
                            st.image(tomek_gif, width=540)
                        elif lw == 'Pawel z Sacza' and os.path.exists(pawel_gif):
                            st.image(pawel_gif, width=540)
                        elif st.session_state.last_gif:
                            st.image(st.session_state.last_gif, width=540)
                        else:
                            st.info('Brak GIF-a do wyświetlenia.')
                        # Audio dla Pawła z Sacza (jeśli dostępne)
                        if lw == 'Pawel z Sacza':
                            pawel_audio = os.path.join(base_dir, 'gifs', 'pawel', 'audio.mp3')
                            if os.path.exists(pawel_audio):
                                # odtwarzaj tylko raz automatycznie (po wygranej), potem można ręcznie
                                if st.session_state.pawel_sound:
                                    st.audio(pawel_audio)
                                    st.session_state.pawel_sound = False
                                # przycisk do ponownego odtworzenia
                                if st.button('🔊 Zagraj dźwięk jeszcze raz', key='pawel_replay'):
                                    st.audio(pawel_audio)
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
            st.session_state.initial_count = None
            st.session_state.tom_target_draw = None
else:
    st.info("Wpisz opcje i zatwierdź, aby rozpocząć zabawę!")
