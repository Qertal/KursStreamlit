import streamlit as st
import os

# dir_path = os.path.join(os.getcwd(), 'tablo', 'zdradzonych')
dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'zdradzonych')


if not os.path.isdir(dir_path):
    st.error(f"Katalog z obrazami nie istnieje: {dir_path}")
else:
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    images = []
    for f in files:
        base = os.path.splitext(f)[0]
        parts = base.split('_', 1)
        if len(parts) == 2:
            id_part, name = parts
            try:
                id_num = int(id_part)
            except ValueError:
                id_num = None
        else:
            id_num = None
            name = parts[0]
        images.append((id_num if id_num is not None else float('inf'), name, f))

    images.sort(key=lambda x: x[0])

    st.title('Tablo zdradzonych')

    for i in range(0, len(images), 3):
        row = images[i:i+3]
        cols = st.columns(3)
        for j, (_, name, filename) in enumerate(row):
            with cols[j]:
                img_path = os.path.join(dir_path, filename)
                st.image(img_path, caption=name, use_container_width=True)