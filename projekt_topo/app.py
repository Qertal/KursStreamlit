import streamlit as st

def home_page():
    st.title("Witamy na stronie głównej")

    st.subheader("Korzystając z panelu z lewej strony, możesz przenieść się do interesującej Cię zakładki.")

### Main page
home = st.Page(home_page, title = 'Strona Główna', icon='🏠')

### Interior

diam = st.Page("pages/set_diam.py", title = 'Średnica zbioru', icon='📐')
dist = st.Page("pages/set_dist.py", title = 'Odległość między zbiorami', icon='🛣️')
ball = st.Page("pages/ball_d2.py", title = 'Kula na płaszczyźnie', icon='⚽️')

### About page
authours = st.Page("pages/about.py", title = 'Autorzy', icon='📋')

pg = st.navigation(
    {
        "Home": [home],
        'Metryka': [diam, dist, ball],
        'O autorach': [authours]
    }
)

pg.run()