import streamlit as st
import pymongo
import pandas as pd
import datetime
# streamlit run main.py --server.port 8503

#App Title
st.title('Dataset')

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()
db = client["Skripsi"]
# sk_sumsel = db["SK_SUMSEL"]

station_dict = {
    "SK_SUMSEL": "Stasiun Klimatologi Sumatera Selatan",
    "SK_SUMUT": "Stasiun Klimatologi Sumatera Utara",
    "SM_BINAKA": "Stasiun Meteorologi Binaka",
    "SM_KUALANAMU": "Stasiun Meteorologi Kualanamu",
    "SM_MINANGKABAU": "Stasiun Meteorologi Minangkabau",
    "SM_SULTAN": "Stasiun Meteorologi Sultan Mahmud Badaruddin II",
    "SM_TOBING": "Stasiun Meteorologi FL Tobing"
}

inv_station_dict = {
    "Stasiun Klimatologi Sumatera Selatan": "SK_SUMSEL",
    "Stasiun Klimatologi Sumatera Utara": "SK_SUMUT",
    "Stasiun Meteorologi Binaka": "SM_BINAKA",
    "Stasiun Meteorologi Kualanamu": "SM_KUALANAMU",
    "Stasiun Meteorologi Minangkabau": "SM_MINANGKABAU",
    "Stasiun Meteorologi Sultan Mahmud Badaruddin II": "SM_SULTAN",
    "Stasiun Meteorologi FL Tobing": "SM_TOBING"
}

var_dict = {
    "Tn": "Temperatur minimum",
    "Tx": "Temperatur maksimum",
    "Tavg": "Temperatur rata-rata",
    "RH_avg": "Kelembapan rata-rata",
    "RR": "Curah hujan",
    "ss": "Lamanya penyinaran matahari",
    "ff_x": "Kecepatan angin maksimum",
    "ff_avg": "Kecepatan angin rata-rata",
}

inv_var_dict = {
    "Temperatur minimum": "Tn",
    "Temperatur maksimum": "Tx",
    "Temperatur rata-rata": "Tavg",
    "Kelembapan rata-rata": "RH_avg",
    "Curah hujan": "RR",
    "Lamanya penyinaran matahari": "ss",
    "Kecepatan angin maksimum": "ff_x",
    "Kecepatan angin rata-rata": "ff_avg",
}

var_data = {
    "Variable": ["Tn", "Tx", "Tavg", "RH_avg", "RR", "ss", "ff_x", "ff_avg"],
    "Description": [
        "Temperatur minimum",
        "Temperatur maksimum",
        "Temperatur rata-rata",
        "Kelembapan rata-rata",
        "Curah hujan",
        "Lamanya penyinaran matahari",
        "Kecepatan angin maksimum",
        "Kecepatan angin rata-rata",
    ],
    "Unit": ["°C", "°C", "°C", "%", "mm", "jam", "m/s", "m/s"]
}

# Convert to DataFrame
var_df = pd.DataFrame(var_data)

station_key_list = list(station_dict.values())

# Create a dropdown input
selected_station = st.selectbox(
    "Select a Station",
    station_key_list,
    index=None,
    placeholder="Select a Station"
)

if selected_station is not None:
    chosen_station = db[str(inv_station_dict[selected_station])]
    resulting = chosen_station.find()
    data_list = list(resulting)
    data_df = pd.DataFrame(data_list)
    data_df = data_df.drop('_id',axis = 1 )
    data_df['Tanggal'] = data_df['Tanggal'].dt.strftime("%d-%m-%Y")

    
    st.dataframe(data_df, hide_index=True, on_select="ignore")

st.dataframe(var_df, hide_index=True)