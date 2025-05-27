import streamlit as st
import os
import streamlit.components as stc

import base64
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

from PIL import Image
import pandas as pd
from docx import Document

#import io

@st.cache_data
def load_image(image_file):
    image = Image.open(image_file)
    image.load()  # Wczytuje wszystkie dane – ważne dla niektórych formatów
    return image.copy()  # Kopia obrazu odcina powiązania z oryginalnym źródłem

# function to save uploaded file to directory
def save_uploaded_file(uploadedfile):
    with open(os.path.join("tempDir",uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success(f"Saved file: {uploadedfile.name} in tempDir.")

def text_downloader(raw_text):
    b64 = base64.b64encode(raw_text.encode()).decode()
    new_filename = f"new_text_file_{timestr}_.txt"
    st.markdown(" #### Download file ###")
    href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click here!!</a>'
    st.markdown(href, unsafe_allow_html=True)


def csv_downloader(data):
    csvfile = data.to_csv()
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = f"new_text_file_{timestr}_.csv"
    st.markdown(" #### Download file ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click here!!</a>'
    st.markdown(href, unsafe_allow_html=True)

class FileDownloader(object):
    """
    >>> download = FileDownloader(data,filename,file_ext).download()
    """
    def __init__(self, data, filename = 'myfile', file_ext='txt'):
        super(FileDownloader, self).__init__()
        self.data = data
        self.filename = filename
        self.file_ext = file_ext

    def download(self):
        b64 = base64.b64encode(self.data.encode()).decode()
        new_filename = f"{self.filename}_{timestr}_.{self.file_ext}"
        st.markdown(" #### Download file ###")
        href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">Click here!!</a>'
        st.markdown(href, unsafe_allow_html=True)



def main():
    st.title("File upload tutorial")

    menu = ['Home','Dataset','Multiple Files','DocumentFiles','About']

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        my_text = st.text_area("Your Message")
        if st.button("Save"):
            st.write(my_text)
            # text_downloader(my_text)
            download = FileDownloader(my_text).download()

        image_file = st.file_uploader("Upload images", 
                                      type=['png','jpg','jpeg'])
        if image_file is not None:
            #To see details
            st.write(type(image_file))
            #methods, attributes
            st.write(dir(image_file))

            file_details = {
                "filename": image_file.name,
                "filetype": image_file.type,
                "filesize": image_file.size
            }
            st.write(file_details)

            st.image(load_image(image_file), width=250)

            #Saving file
            # tempDir/Imagename.png

            with open(os.path.join("tempDir",image_file.name),"wb") as f:
                f.write(image_file.getbuffer())

            st.success("File Saved")



    elif choice == "Dataset":
        st.subheader("Dataset")
        data_file = st.file_uploader("Upload CSV", type=['csv'])
        if data_file is not None:
            st.write(type(data_file))
            df = pd.read_csv(data_file)
            st.dataframe(df)

            file_details = {
                "filename": data_file.name,
                "filetype": data_file.type,
                "filesize": data_file.size
            }
            st.write(file_details)

            save_uploaded_file(data_file)

            # csv_downloader(df)

            download = FileDownloader(df.to_csv(),file_ext='csv').download()

    elif choice == "Multiple Files":
        st.title("Multiple file uploads app")
        
        st.subheader("Upload multiple files")

        uploaded_files = st.file_uploader("Upload Multiple Images", type =['png','jpeg','jpg'], accept_multiple_files=True)
        if uploaded_files is not None:
            st.write(uploaded_files)
            for image_file in uploaded_files:
                st.write(image_file.name)
                st.image(load_image(image_file), width=250)
                # save individual file
                save_uploaded_file(image_file)

    elif choice == "DocumentFiles":
        st.subheader("DocumentFiles")

        docx_file = st.file_uploader("Upload DOCX file",
                                     type=['pdf','docx','txt'])
        if st.button("Process"):
            if docx_file is not None:

                file_details = {
                    "filename": docx_file.name,
                    "filetype": docx_file.type,
                    "filesize": docx_file.size
                }

                st.write(file_details)

                if docx_file.type == "text/plain":
                    # Read as bytes
                    raw_text = docx_file.read()
                    st.write(raw_text) #works but in bytes
                    st.text(raw_text) # does work as expected
                    #read as string (decode bytes to string)
                    # raw_text2 = str(docx_file.read(),'utf-8')
                    raw_text = raw_text.decode('utf-8')
                    st.write(raw_text) #works
                    st.text(raw_text) #works
                elif docx_file.type == "application/pdf":
                    pass
                # else:
                #     raw_text =
                #     st.write(raw_text)

                #     st.text(raw_text)





    else:
        st.subheader("About")

if __name__ == '__main__':
    main()