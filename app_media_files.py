import streamlit as st

#working media files(videos/images/audio)

#display images

from PIL import Image
img = Image.open("data/image_03.jpg")
st.image(img, use_column_width=True)

# from url
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTU6Z2DFD5BZcETRmBfNvqnQORkZCTe7bTLJQ&s", use_column_width=True)

# videos

video_file = open("data/secret_of_success.mp4","rb").read()
st.video(video_file, start_time=3)

# display audio/working with audio

audio_file = open("data/song.mp3", "rb")
st.audio(audio_file.read())