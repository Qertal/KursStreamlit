import streamlit as st

import pandas as pd
import joblib
import os

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import plotly.express as px

@st.cache_resource
def load_data(data):
    df = pd.read_csv(data)
    return df

def run_eda_app():
    st.title("Exploratory Data Analysis (EDA)")
    # df = pd.read_csv("data/diabetes_data_upload.csv")
    df = load_data("data/diabetes_data_upload.csv")
    df_encoded = load_data("data/diabetes_data_upload_clean.csv")
    freq_df = load_data("data/freqdist_of_age_data.csv")

    submenu = st.sidebar.selectbox("Submenu",
                                   ["Descriptive", "Plots"])
    
    if submenu == "Descriptive":
        st.dataframe(df)

        with st.expander("Data Description"):
            st.write(df.dtypes)

        with st.expander("Data describe"):
            st.write(df_encoded.describe())
        
        with st.expander("Classes distribution"):
            st.write(df['class'].value_counts())

        with st.expander("Gender distribution"):
            st.write(df['Gender'].value_counts())

    elif submenu == 'Plots':
        st.subheader("Plots")
        st.write("This section contains plots for the EDA.")

        col1, col2 = st.columns([2,1])

        with col1:
            with st.expander("Dist plot of gender"):
                fig = plt.figure()
                sns.countplot(df['Gender'])
                st.pyplot(fig)

                gen_df = df['Gender'].value_counts().to_frame()
                gen_df = gen_df.reset_index()
                gen_df.columns = ['Gender type', 'Count']
                # st.dataframe(gen_df)

                p1 = px.pie(gen_df, names='Gender type', values='Count')
                st.plotly_chart(p1, use_container_width=True)

            with st.expander("Dist plot of class"):
                fig = plt.figure()
                sns.countplot(df['class'])
                st.pyplot(fig)


        with col2:
            with st.expander("Gender distribution"):
                st.dataframe(gen_df)

            with st.expander("Class distribution"):
                class_df = df['class'].value_counts().to_frame()
                class_df = class_df.reset_index()
                class_df.columns = ['Class type', 'Count']
                st.dataframe(class_df)

        with st.expander("Frequency distribution"):
            st.dataframe(freq_df)
            # st.write(freq_df.columns)
            p2 = px.bar(freq_df, x='Age', y='count', color='count', title="Frequency Distribution of Age")
            st.plotly_chart(p2, use_container_width=True)

        with st.expander("Outlier detection plot"):
            fig = plt.figure(figsize=(10, 8))
            sns.boxplot(data=df['Age'], orient="h")
            st.pyplot(fig)

            p3 = px.box(df, x='Age',color='Gender', points="outliers" , title="Outlier detection plot")
            st.plotly_chart(p3, use_container_width=True)

        with st.expander("Correlation heatmap"):
            fig = plt.figure(figsize=(10, 8))
            sns.heatmap(df_encoded.corr(), annot=True, cmap='coolwarm')
            st.pyplot(fig)

            p4 = px.imshow(df_encoded.corr(), title="Correlation heatmap")
            st.plotly_chart(p4)

        # with st.expander("Correlation heatmap"):
        #     plt.figure(figsize=(10, 8))
        #     sns.heatmap(df_encoded.corr(), annot=True, cmap='coolwarm')
        #     st.pyplot(plt)

        # with st.expander("Pairplot"):
        #     sns.pairplot(df_encoded, hue='class')
        #     st.pyplot(plt)

        # with st.expander("Class distribution bar plot"):
        #     fig = px.histogram(df, x="class", color="class", title="Class Distribution")
        #     st.plotly_chart(fig)