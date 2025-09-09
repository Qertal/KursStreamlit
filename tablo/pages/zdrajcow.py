import streamlit as st
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "zdrajcow"

if not DATA_DIR.exists():
    st.error(f"Nie znaleziono katalogu z danymi: {DATA_DIR}")
    st.stop()

files = sorted([p for p in DATA_DIR.iterdir() if p.is_file()])
st.write(f"Znaleziono {len(files)} plików w {DATA_DIR}")

# files = os.listdir(os.getcwd() + '/zdrajcow/')

members = {}
for i in files:
    member = os.path.splitext(i)[0].split('_')
    members[member[0]] = member[1], i, int(member[0])%3

col0, col1, col2 = st.columns([3,2,3])

with col1:
    st.title('Tablo zdrajców')

for id, (name, filename, column) in members.items():
    # st.image('zdrajcow/' + filename, caption=name)
    if column == 0:
        col0, col1, col2 = st.columns(3)
    if column == 0:
        with col0:
            st.image(str(DATA_DIR / filename), caption=name, use_container_width=True)
    elif column == 1:
        with col1:
            st.image(str(DATA_DIR / filename), caption=name, use_container_width=True)
    else:
        with col2:
            st.image(str(DATA_DIR / filename), caption=name, use_container_width=True)