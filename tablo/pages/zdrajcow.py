import streamlit as st
import os
import re

base_dir = os.path.join(os.getcwd(), 'tablo', 'zdrajcow')
if not os.path.isdir(base_dir):
    st.error(f"Directory not found: {base_dir}")
    st.stop()

# only keep common image extensions
files = [f for f in os.listdir(base_dir) if re.search(r'\.(jpg|jpeg|png|gif)$', f, re.I)]

members = {}
for i in files:
    name_part, _ = os.path.splitext(i)
    parts = name_part.split('_', 1)
    if len(parts) != 2:
        # skip files that don't match '<id>_<name>.<ext>'
        continue
    member_id, member_name = parts
    try:
        column = int(member_id) % 3
    except ValueError:
        # skip non-numeric ids
        continue
    members[member_id] = (member_name, i, column)

col0, col1, col2 = st.columns([3,2,3])

with col1:
    st.title('Tablo zdrajców')

cols = (col0, col1, col2)

# iterate in numeric order of ids
for member_id, (name, filename, column) in sorted(members.items(), key=lambda x: int(x[0])):
    with cols[column]:
        st.image(os.path.join('tablo', 'zdrajcow', filename), caption=name, use_container_width=True)