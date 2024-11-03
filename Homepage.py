import streamlit as st

user_name = st.session_state['name']
st.subheader(f'Selamat Datang, {user_name}')

st.write('Website ini dibuat dengan tujuan untuk melakukan prediksi terhadap data meteorologi di Pulau Sumatra.\n'
         )

st.write('Prediksi dilakukan menggunakan algoritma Gated Recurrent Unit (GRU) dan Random Forest berdasarkan data meteorologi yang dikumpulkan dari 7 stasiun meteorologi yang tersebar di Pulau Sumatra dari tanggal 1 Januari 2000 samapai dengan 30 Juni 2024')