import streamlit as st
import pandas as pd
import time
import plotly.express as px
import streamlit.components.v1 as components


#text element

st.text("This is a text")

st.title("This is a title:H")

st.subheader("This is a subheader")

st.header("This is a header")

st.write("This is a super function")

st.markdown("""THIS IS *MARKDOWN*""")

st.latex("\int")

st.json("""{"data":"This is streamlit"}""")

st.code("""
print("hello streamlit")
a=40
""",language="python", line_numbers=True)

st.success("This is success")
st.error("error")
st.warning("warning")
st.exception("exception")

# input widhget

first_name = st.text_input("First Name")
password = st.text_input("Password",type='password')
message = st.text_area("Message")

date=st.date_input("Date")

appointment_time = st.time_input("Time")

age = st.number_input("Age", min_value=0, max_value=120)
gender = st.radio("Gender",['Male','Female'])
enable = st.toggle("Enable picker")
level = st.checkbox("Level")

#sliders and selectors

countries = st.selectbox("Countries",["USA","Poland","Germany"])
programming_languages = st.multiselect("Programmin",["Python","Go","Java"])
rating = st.slider("Rating",0,10)
ranking = st.select_slider("Ranking",['Junior Dev','Dev','Senior Dev'])

st.divider()
if enable:
    st.write(f'Details:{first_name},{password}')
    color = st.color_picker("Pick a Color")
    st.write(color)

#data elements
def load_data(data) -> pd.DataFrame:
    return pd.read_csv(data)

df = load_data("iris.csv")
st.dataframe(df)
st.table(df.head())

edited_data = st.data_editor(df)
st.json(df.to_json())

# connection to db

# st.connection()

# Media elements

img = st.image("Facebook_logo.png", caption="Image in streamlit")

audio = open("data/song.mp3",'rb')
st.audio(audio.read())

#video

# st.video()

enabler = st.toggle("Do you want take a photo?", key="test")
if enabler:
    pic = st.camera_input("Take a photo")
    if pic is not None:
        with open(f"{pic.name}","wb") as f:
            f.write(pic.getbuffer())

#downlaod and upload 
file_upload = st.file_uploader("Upload CSV", type='csv')
if file_upload:
    st.write(pd.read_csv(file_upload))

st.download_button("Download","iris.csv")

# status elements
if st.button("Compute"):
    progress_bar = st.progress(0)
    with st.spinner("Thinking..."):
        for i in range(101):
            time.sleep(0.03)
            progress_bar.progress(i)
        st.write("Hello")

    # with st.progress(value=range(0,100)):
    #     time.sleep(1)
    #     st.write("Hello")

    st.toast("This is a toast")
    st.balloons()

# Create a progress bar

# progress_bar = st.progress(0)

# with st.spinner("Processing..."):
#     for i in range(101):
#         time.sleep(0.03)
#         progress_bar.progress(i)

#chat elements (LLM UI)
#typewriter effect
def stream_data(data,delay:float=0.1):
    for word in data.split():
        yield word + " "
        time.sleep(delay)

prompt = st.chat_input("Ask something")
if prompt:
    with st.chat_message("AI"):
        st.write(f'bot typed {prompt}')

    with st.spinner("Thinking"):
        time.sleep(1)
        response = f'some random text from streamlit'
        # with st.chat_message("User"):
        #     st.write(response)
        st.write_stream(stream_data(response))

#streaming response
#generator
#some text or data


response = f'some random text from streamlit'
# with st.chat_message("User"):
#     st.write(response)
if st.button("Stream"):
    st.write_stream(stream_data(response))

st.divider()

### layouts

#tabs
home_tab, about_tab = st.tabs(["Home","About"])

with home_tab:
    st.subheader("This is home tab")

with about_tab:
    st.subheader("This is about tab")
    st.dataframe(df)

#columns 

col1, col2 = st.columns(2)
#contect manager approach

with col1:
    st.title("Columns")

col2.dataframe(df)

col2.image('Facebook_logo.png', use_container_width=True)

# container 

container = st.container(border=True)
container.write("container")

row1 = st.columns(3)
row2 = st.columns(2)

for col in row1+row2:
    tile = col.container(height=128)
    tile.title(":balloon:")

#expander and popover

with st.expander("Expander"):
    st.dataframe(df)

with st.popover("Popover"):
    st.image("Facebook_logo.png")

### plots

st.area_chart(df, x="sepal_length", y="petal_length")
st.line_chart(df, x="sepal_length", y="petal_length")

st.bar_chart(df, x="sepal_length", y="petal_length")

st.vega_lite_chart(df, x="sepal_length", y="petal_length")

st.scatter_chart(df, x="sepal_length", y="petal_length")

# st.pyplot()

fig_plotly = px.scatter(
    df,
    x="sepal_length",
    y="sepal_width",
    color="species",
    title="Plotly: Sepal Length vs Width"
)

st.plotly_chart(fig_plotly)

import altair as alt

chart_altair = alt.Chart(df).mark_circle(size=60).encode(
    x="sepal_length",
    y="sepal_width",
    color="species",
    tooltip=["sepal_length", "sepal_width", "species"]
).interactive()

st.altair_chart(chart_altair, use_container_width=True)

import numpy as np

df_map = df.copy()
df_map["lat"] = np.random.uniform(50.0, 50.1, len(df))
df_map["lon"] = np.random.uniform  (19.9, 20.1, len(df))

st.map(df_map.rename(columns={"lat": "latitude", "lon": "longitude"}))


#
# st.map(df)
# st.plotly_chart()
# st.altair_chart()
# st.bokeh_chart()

st.help(st.pyplot)
st.write(dir(st))

#st form

st.html("<p> jebac dydy </p>")
components.iframe("https://www.wikipedia.org", width=800, height=800, scrolling = True)
st.link_button("visit",url="https://udemy.com/")

# st.session_state
#st.cache_data