import streamlit as st
from streamlit_gsheets import GSheetsConnection

import pandas as pd
from ydata_profiling import ProfileReport

from streamlit_pandas_profiling import st_profile_report

#for plotting images & adjusting colors
import matplotlib.pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud , STOPWORDS, ImageColorGenerator
from PIL import Image
import plotly.express as px


st.set_page_config(
    page_title="Data profiler",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("<h1 style='text-align: center;'> Data Profiler App </h1>",
            unsafe_allow_html=True)
st.markdown("----")

conn = st.connection("gsheet", type=GSheetsConnection)

df = conn.read(
    spreadsheet = st.secrets.gsheet_promotion["spreadsheet"],
    worksheet = st.secrets.gsheet_promotion["worksheet"]
    )

    
text = df.job_title.tolist() 

# join the list and lowercase all the words
text = ' '.join(text).lower()


#create the wordcloud object
wordcloud = WordCloud(stopwords = STOPWORDS,
                     collocations=True,
                     min_word_length =3,
                     background_color='white').generate(text)


#text_dictionary = wordcloud.process_text(text)

#wordcloud = WordCloud(min_word_length =3,
#                      background_color='white').generate(text_dictionary)


#plot

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
st.pyplot()


fig = px.bar(df['employee_residence'].value_counts())
fig.update_layout(showlegend=False,
                   xaxis_title="Country",
                   yaxis_title="Employee Number")
#st.write(fig)

# Visualisasi interaktif
fig2 = px.bar(df['company_location'].value_counts())
fig2.update_layout(showlegend=False,
                   xaxis_title="Country",
                   yaxis_title="Employee Number")
#st.write(fig)


col1 , col2 = st.columns(2)
with col1:
    st.subheader("Employee Residence")
    st.write(fig)


with col2:
    st.subheader("Company Location")
    st.write(fig2)




with st.sidebar:
    st.markdown("Employee Data")
    st.markdown("---")

if st.sidebar.button("Start profiling"):

    
    pr = ProfileReport(df)
    st_profile_report(pr)
    
    

