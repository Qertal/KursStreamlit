import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import altair as alt

import plotly.express as px


def main():
    st.title("Plotting with st.pyplot")
    df = pd.read_csv("data/iris.csv")
    df2 = pd.read_csv("data/lang_data.csv")
    df4 = pd.read_csv("data/prog_languages_data.csv")
    st.dataframe(df.head())

    # pref meth

    # df['species'].value_counts().plot(kind='bar')
    # st.pyplot()

    #recommended method
    plt.scatter(*np.random.random(size=(2,100)))
    st.pyplot()

    fig, ax = plt.subplots()
    ax.scatter(*np.random.random(size=(2,100)))
    st.pyplot(fig)

    #method 2: simple method
    fig = plt.figure()
    df['species'].value_counts().plot(kind='bar')
    st.pyplot(fig)

    #method 3
    fig, ax = plt.subplots()
    df['species'].value_counts().plot(kind='bar')
    st.pyplot(fig)

    #alternative for matplotlib

    fig = plt.figure()
    sns.countplot(df['species'])
    st.pyplot(fig)

    #bar chart
    #st bar_chart
    st.bar_chart(df[['sepal_length','petal_length']])

    #line chart
    lang_list = df2.columns.tolist()
    lang_choices = st.multiselect("Choose Language", lang_list, default="C")
    new_df = df2[lang_choices]
    st.line_chart(new_df)

    #area chart

    st.area_chart(new_df, use_container_width=True)

    #altair

    df3 = pd.DataFrame(
        np.random.randn(200,3),
        columns=['a','b','c']
    )
    c = alt.Chart(df3).mark_circle().encode(
        x = 'a',
        y = 'b',
        size = 'c',
        color = 'c',
        tooltip = ['a','b','c']
    )
    st.dataframe(df3.head())

    #meth 1 using st.write
    st.write(c)

    # altair
    st.altair_chart(c)

    st.dataframe(df4)

    fig = px.pie(df4, values='Sum', names = 'lang',title = 'Pie chart')
    st.plotly_chart(fig)

    fig2 = px.bar(df4, x='lang',y = 'Sum')
    st.plotly_chart(fig2)




if __name__ == '__main__':
    main()