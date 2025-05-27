import streamlit as st
import numpy as np
from pages.func import metryka_minkowskiego, macierz_odleglosci, macierz_do_latex
import random

st.title("Średnica zbioru")

st.write("Tutaj, może obliczyć średnicę zbioru, a dodatkowo zobaczyć w jaki sposób wygląa macierz odległości. Wybierz przestrzeń w jakiej chcesz się znajdować oraz p odpowiednie dla konkretnej metryki mińkowskiego, jaka Cię interesuje.")

nieskonczonosc = st.checkbox(label='Metryka maksimum')

if nieskonczonosc == False:
    p = st.number_input(label='Wartość p dla metryki mińkowskiego',min_value=0.01)
else:
    p = float('inf')

col1, col2 = st.columns(2)

with col1 as f:
    n = st.number_input(label="Wybierz n dla przestrzeni", min_value=1, step=1)

with col2 as f:
    l = st.number_input(label="Wybierz liczbę punktów w tej przestrzeni", min_value=1, step=1)


if st.button(label=' Generuj pola', key='fields'):
    st.session_state.fields_generated = True


if st.session_state.get('fields_generated', False):
    with st.form(key='Wprowadzanie'):
        st.latex(fr"\text{{Wprowadź współrzędne dla {int(l)} punktów w przestrzeni }} \mathbb{{R}}^{int(n)}")
        points = np.zeros(shape=(int(l), int(n)))

        for i in range(int(l)):
            st.markdown(f"**Punkt {i + 1}:**")
            num_columns = min(int(n), 5)
            cols = st.columns(num_columns)

            for k in range(int(n)):
                col = cols[k % num_columns]
                with col:
                    points[i, k] = st.number_input(
                        label=f"Wspolrzedna {k + 1}",
                        key=f'coord_{i}_{k}',
                        value=random.randint(0, 15)
                    )

        submitted = st.form_submit_button(label="Oblicz")

    if submitted:
        D, srednica = macierz_odleglosci(points, p)
        # st.success("✅ Wyniki obliczeń:")
        st.write(" **Macierz odległości:**")
        # st.table(np.round(D, 2))

        # macierz_txt = "\n".join(
        # ["\t".join([f"{val:.2f}" for val in row]) for row in D]
        # )
        # st.text("Macierz odległości:")
        # st.code(macierz_txt)

        st.latex(macierz_do_latex(np.round(D, 2)))
        st.write(f" **Średnica zbioru:** `{srednica:.4f}`")

