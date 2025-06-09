import streamlit as st
import numpy as np
from pages.func import odleglosc_miedzy_zbiorami

# --- Inicjalizacja session_state ---
defaults = {
    "fields_generated": False,
    "points_E": None,
    "points_F": None,
    "p": 2.0,
    "nieskonczonosc": False,
    "n": 1,
    "l_E": 1,
    "l_F": 1
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- Tytuł i opis ---
st.title("Odległość między zbiorami: Przygotowanie danych")

st.markdown(r"""
Wygeneruj punkty dwóch zbiorów $ E $ i $ F $ w przestrzeni $ \mathbb{R}^n $.
""")

# --- Metryka maksimum ---
st.session_state.nieskonczonosc = st.checkbox(
    'Metryka maksimum (p = ∞)',
    value=st.session_state.nieskonczonosc
)

if not st.session_state.nieskonczonosc:
    st.session_state.p = st.number_input(
        'Wartość p dla metryki Minkowskiego',
        min_value=0.01,
        value=1.0
    )
else:
    st.session_state.p = float('inf')

# --- Parametry przestrzeni ---
col1, col2, col3 = st.columns(3)

with col1:
    st.session_state.n = st.number_input("Wymiar przestrzeni (n)", min_value=1, step=1, value=st.session_state.n)

with col2:
    st.session_state.l_E = st.number_input("Liczba punktów zbioru E", min_value=1, step=1, value=st.session_state.l_E)

with col3:
    st.session_state.l_F = st.number_input("Liczba punktów zbioru F", min_value=1, step=1, value=st.session_state.l_F)

# --- Przycisk generowania punktów ---
if st.button("Generuj punkty"):
    st.session_state.fields_generated = True
    st.session_state.points_E = np.random.randint(-15, 15, size=(int(st.session_state.l_E), int(st.session_state.n))).astype(float)
    st.session_state.points_F = np.random.randint(-15, 15, size=(int(st.session_state.l_F), int(st.session_state.n))).astype(float)

# --- Wprowadzanie punktów ---
def wprowadz_punkty(label, l, points, prefix):
    st.subheader(f"Wprowadź współrzędne {l} punktów w przestrzeni $ \mathbb{{R}}^{st.session_state.n} $")
    for i in range(l):
        st.markdown(f"**Punkt {i + 1}:**")
        cols = st.columns(min(st.session_state.n, 5))
        for k in range(st.session_state.n):
            col = cols[k % len(cols)]
            with col:
                key = f'{prefix}_{i}_{k}'
                val = st.number_input(
                    label=f"x{k + 1}",
                    key=key,
                    value=int(points[i, k]),
                    step = 1
                )
                points[i, k] = st.session_state[key]
    return points

if st.session_state.fields_generated:
    if (st.session_state.points_E is None or
        st.session_state.points_E.shape != (int(st.session_state.l_E), int(st.session_state.n)) or
        st.session_state.points_F is None or
        st.session_state.points_F.shape != (int(st.session_state.l_F), int(st.session_state.n))):
        st.warning("Zmieniono parametry. Kliknij ponownie 'Generuj punkty'.")
    else:
        with st.form("form_wprowadzanie"):
            st.markdown("### Zbiór E")
            st.session_state.points_E = wprowadz_punkty("Zbiór E", st.session_state.l_E, st.session_state.points_E, "E")

            st.markdown("### Zbiór F")
            st.session_state.points_F = wprowadz_punkty("Zbiór F", st.session_state.l_F, st.session_state.points_F, "F")

            submitted = st.form_submit_button("Oblicz odległość")

        if submitted:
            st.success("Dane punktów zbiorów E i F zostały zapisane.")
            st.write("Punkty zbioru **E**:")
            st.write(st.session_state.points_E)

            st.write("Punkty zbioru **F**:")
            st.write(st.session_state.points_F)

            dist = odleglosc_miedzy_zbiorami(st.session_state.points_E, st.session_state.points_F, st.session_state.p)

            st.write("**Odległość między zbiorami E i F:**")
            st.latex(f"d(E, F) = {dist:.4f}")

            print(f"Odległość między zbiorami E i F: {dist:.4f}")