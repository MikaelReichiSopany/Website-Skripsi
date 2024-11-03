import streamlit as st
import pymongo
import pandas as pd


df_gru = pd.read_excel('model_summary/gru.xlsx')
df_rf = pd.read_excel('model_summary/rf.xlsx')

st.subheader('Model summary for GRU')
st.dataframe(df_gru, hide_index=True)

st.write("TimeStep = Jumlah hari sebagai input data.")
st.write("Optimizer = Algoritma yang digunakan untuk mengoptimalkan bobot dalam model.")
st.write("Learning Rate = Ukuran langkah yang diambil saat mengupdate bobot model.") 
st.write("Units = Jumlah neuron.") 
st.write("Batch Size = Jumlah sampel data yang diproses dalam satu iterasi pelatihan.") 
st.write("Activation Function = Fungsi matematika yang diterapkan pada output dari suatu neuron dalam jaringan saraf tiruan.") 
st.write("Epochs = Jumlah iterasi pelatihan yang dilakukan.") 




st.subheader('Model summary for Random Forest')
st.dataframe(df_rf, hide_index=True)

st.write("TimeStep = Jumlah hari sebagai input data.")
st.write("N_estimatos = Jumlah decision tree.")
st.write("max_depth = Kedalaman maksimum setiap decision tree.")
st.write("min_samples_split = Jumlah data minimum yang diperlukan untuk membagi sebuah node dalam pohon.")
st.write("min_samples_leaf = Jumlah data minimum yang diizinkan dalam sebuah node daun.")
st.write("max_features =  Jumlah fitur yang dipertimbangkan pada setiap pembagian dalam pohon.")
st.write("criterion =  Metrik yang digunakan untuk mengevaluasi kualitas pembagian.")
