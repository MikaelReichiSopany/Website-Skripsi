import streamlit as st
import pymongo
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
    "SK_SUMSEL": "Stasiun Klimatologi Sumatera Selatan (Palembang)",
    "SK_SUMUT": "Stasiun Klimatologi Sumatera Utara (Deli Serdang)",
    "SM_BINAKA": "Stasiun Meteorologi Binaka (Nias)",
    "SM_KUALANAMU": "Stasiun Meteorologi Kualanamu (Deli Serdang)",
    "SM_MINANGKABAU": "Stasiun Meteorologi Minangkabau (Padang Pariaman)",
    "SM_SULTAN": "Stasiun Meteorologi Sultan Mahmud Badaruddin II (Palembang)",
    "SM_TOBING": "Stasiun Meteorologi FL Tobing (Tapanuli Tengah)"
}

inv_station_dict = {
    "Stasiun Klimatologi Sumatera Selatan (Palembang)": "SK_SUMSEL",
    "Stasiun Klimatologi Sumatera Utara (Deli Serdang)": "SK_SUMUT",
    "Stasiun Meteorologi Binaka (Nias)": "SM_BINAKA",
    "Stasiun Meteorologi Kualanamu (Deli Serdang)": "SM_KUALANAMU",
    "Stasiun Meteorologi Minangkabau (Padang Pariaman)": "SM_MINANGKABAU",
    "Stasiun Meteorologi Sultan Mahmud Badaruddin II (Palembang)": "SM_SULTAN",
    "Stasiun Meteorologi FL Tobing (Tapanuli Tengah)": "SM_TOBING"
}

# inv_station_dict = {
#     "Stasiun Klimatologi Sumatera Selatan": "SK_SUMSEL",
#     "Stasiun Klimatologi Sumatera Utara": "SK_SUMUT",
#     "Stasiun Meteorologi Binaka": "SM_BINAKA",
#     "Stasiun Meteorologi Kualanamu": "SM_KUALANAMU",
#     "Stasiun Meteorologi Minangkabau": "SM_MINANGKABAU",
#     "Stasiun Meteorologi Sultan Mahmud Badaruddin II": "SM_SULTAN",
#     "Stasiun Meteorologi FL Tobing": "SM_TOBING"
# }

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

target_cols = [
    ('Tn', '°C'),
    ('Tx', '°C'),
    ('Tavg', '°C'),
    ('RH_avg', '%'),
    ('RR', 'mm'),
    ('ss', 'jam'),
    ('ff_x', 'm/s'),
    ('ff_avg', 'm/s')
]

format_dict = {
    "Temperatur minimum": "{:.2f} °C",
    "Temperatur maksimum": "{:.2f} °C",
    "Temperatur rata-rata": "{:.2f} °C",
    "Kelembapan rata-rata": "{:.2%}",
    "Curah hujan": "{:.2f} mm",
    "Lamanya penyinaran matahari": "{:.2f} jam",
    "Kecepatan angin maksimum": "{:.2f} m/s",
    "Kecepatan angin rata-rata": "{:.2f} m/s"
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
    with st.spinner('Loading...'):
    

        chosen_station = db[str(inv_station_dict[selected_station])]
        resulting = chosen_station.find()
        data_list = list(resulting)
        data_df = pd.DataFrame(data_list)
        data_df = data_df.drop('_id',axis = 1 )

        img_df = data_df.set_index('Tanggal').copy()
        data_df['Tanggal'] = data_df['Tanggal'].dt.strftime("%d-%m-%Y")
        data_df = data_df.set_index('Tanggal')

        
        rename_dict = dict(zip(data_df.columns, var_data["Description"]))
        result_df = data_df.rename(columns=rename_dict)
        result_df["Kelembapan rata-rata"] = result_df["Kelembapan rata-rata"] / 100

        st.dataframe(result_df.style.format(format_dict))


        for col, unit in target_cols:
            plt.figure(figsize=(15, 5))
            plt.plot(img_df.index.to_numpy(), img_df[col].to_numpy(), label=col)
            plt.title(var_dict[col])
            plt.xlabel('Date')
            plt.ylabel('Values in ' + unit)
            # plt.legend(loc='upper right')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.gca().xaxis.set_major_locator(mdates.YearLocator(1))  # Show tick every year
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format the date as 'YYYY'
            st.pyplot(plt)
            # plt.show()

