import streamlit as st
import pymongo
import pandas as pd


df_gru = pd.read_excel('model_summary/GRU.xlsx')
df_rf = pd.read_excel('model_summary/RF.xlsx')

st.subheader('Model summary for GRU')
st.dataframe(df_gru)
st.subheader('Model summary for Random Forest')
st.dataframe(df_rf)