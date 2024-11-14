import streamlit as st
import joblib
import datetime
import numpy as np
import pandas as pd
import pymongo
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# inv_station_dict = {
#     "Stasiun Klimatologi Sumatera Selatan": "SK_SUMSEL",
#     "Stasiun Klimatologi Sumatera Utara": "SK_SUMUT",
#     "Stasiun Meteorologi Binaka": "SM_BINAKA",
#     "Stasiun Meteorologi Kualanamu": "SM_KUALANAMU",
#     "Stasiun Meteorologi Minangkabau": "SM_MINANGKABAU",
#     "Stasiun Meteorologi Sultan Mahmud Badaruddin II": "SM_SULTAN",
#     "Stasiun Meteorologi FL Tobing": "SM_TOBING"
# }

# station_dict = {
#     "SK_SUMSEL": "Stasiun Klimatologi Sumatera Selatan",
#     "SK_SUMUT": "Stasiun Klimatologi Sumatera Utara",
#     "SM_BINAKA": "Stasiun Meteorologi Binaka",
#     "SM_KUALANAMU": "Stasiun Meteorologi Kualanamu",
#     "SM_MINANGKABAU": "Stasiun Meteorologi Minangkabau",
#     "SM_SULTAN": "Stasiun Meteorologi Sultan Mahmud Badaruddin II",
#     "SM_TOBING": "Stasiun Meteorologi FL Tobing"
# }

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

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)


start_date_limit = datetime.date(2024, 6, 30)

def my_reshape (dataset, time_step):
  dataX = []
  a = dataset[0:(0 + time_step), :]
  dataX.append(a)
  return np.array(dataX)

def predict(station, date, algorithm, start_date = None):

  chosen_station = db[str(inv_station_dict[station])]

  initial_data = chosen_station.find().sort({ 'Tanggal': -1 }).limit(14)

  loop_days = (date - start_date_limit).days

# change mongodb object to df
  data_list = list(initial_data)
  data_df = pd.DataFrame(data_list)
  data_df = data_df.drop('_id',axis = 1 )
  data_df = data_df.iloc[::-1]
  data_df = data_df.set_index('Tanggal')

  if algorithm == 'GRU':

    best_model = [4, 6, 7, 8]
    best_model_number = [4, 8, 7, 7, 6, 7, 4, 8]
    # # Iterative forecasting
    date_for_index = start_date_limit
    scaler = joblib.load(f'GRU_Model/scaler.joblib')

    for _ in range(loop_days):

      result_dict = {}
      for i in best_model:
        # uwu
        model = joblib.load(f'GRU_Model/gru_{i}.joblib')
        
        if i == 6:
          time_step = 7
        else:
          time_step = 14 

          # # scale data
        scaled_data = scaler.transform(data_df)

        # Make prediction
        pred = model.predict(scaled_data[-time_step:].reshape(1, time_step, -1))  # Adjust shape as needed
        pred = scaler.inverse_transform(pred)
        result_dict[f'{i}'] = pred[0]
        
      date_for_index += datetime.timedelta(days=1)

      list_to_append = []
      list_to_append.append([])

      for i in range(0, len(best_model_number)):
        list_to_append[0].append(result_dict[f'{best_model_number[i]}'][i])
      print(list_to_append)

      pred_df = pd.DataFrame(list_to_append)
      pred_df.index = [date_for_index]
      pred_df.columns = data_df.columns

      data_df = pd.concat([data_df, pred_df])
      print(data_df)

    if start_date:
      range_day = (date - start_date).days
      return data_df[-(range_day + 1):]
    else:
      return data_df[-1:]

  else:
    # load model
    date_for_index = start_date_limit
    for _ in range(loop_days):
      
      date_for_index += datetime.timedelta(days=1)
      all_var_pred = []

      # best_model = [3, 3, 3, 3, 1, 1, 3, 3]
      # best_model = [4, 3, 3, 3, 1, 1, 3, 2]
      best_model = [4, 3, 3, 3, 2, 2, 3, 2]
      counter = 0
      for var, desc in  var_dict.items():

        model = joblib.load(f'RF_Model/{best_model[counter]}_{var}.joblib')
        if best_model[counter] == 2:
          time_step = 7
        else:
          time_step = 14
        counter += 1
        prep_data = my_reshape(data_df[-time_step:].values, time_step)

        pred = model.predict(prep_data.reshape(prep_data.shape[0], -1))
        all_var_pred.append(pred[0])

      pred_df = pd.DataFrame(all_var_pred)
      pred_df = pred_df.transpose()
      pred_df.columns = data_df.columns
      pred_df.insert(0, 'Tanggal', date_for_index)

      pred_df = pred_df.set_index('Tanggal')

      data_df = pd.concat([data_df, pred_df])

  if start_date:
      range_day = (date - start_date).days
      return data_df[-(range_day + 1):]
  else:
      return data_df[-1:]

client = init_connection()
db = client["Skripsi"]

st.title("Predict")

station_key_list = list(station_dict.values())

selected_station = st.selectbox(
    "Select a Station",
    station_key_list,
    index=None,
    placeholder="Select a Station",
    key='station'
)

date_toggle = st.toggle("Date as a range")

disable_button = False
if not date_toggle:
  selected_date = st.date_input(
      "Select a Date",
      value=None,
      format = "DD/MM/YYYY",
      min_value=start_date_limit + datetime.timedelta(days=1),
      key = 'single_date'
  )
else:
  selected_start_date = st.date_input(
      "Select Starting Date",
      value=None,
      format = "DD/MM/YYYY",
      min_value=start_date_limit + datetime.timedelta(days=1),
      key = 'start_date'
  )

  selected_end_date = st.date_input(
      "Select End Date",
      value=None,
      format = "DD/MM/YYYY",
      min_value=start_date_limit + datetime.timedelta(days=1),
      key = 'end_date'
  )

  if selected_end_date and selected_start_date:
    if selected_end_date <= selected_start_date:
      disable_button = True
      st.error("Selected End Date must be more than Selected Start Date")

selected_algorithm = st.selectbox(
    "Select a algorithm",
    ["GRU", "Random Forest"],
    index=None,
    placeholder="Select a algorithm",
    key='algorithm'
)

if selected_algorithm == 'GRU' :
  model_list = ["Kombinasi Model Terbaik", 1, 2, 3, 4, 5, 6, 7, 8]
else:
  model_list = ["Kombinasi Model Terbaik", 1, 3, 5, 6, 7, 8]


# selected_model = st.selectbox(
#   "Select a Model",
#   model_list,
#   index=None,
#   placeholder="Select a algorithm",
#   key='model'
# )



if not date_toggle:
  bool_button = bool(selected_station and selected_date and selected_algorithm 
                    #  and selected_model
                    )

  predict_button = st.button("Predict", disabled= not bool_button)

  if predict_button:
    with st.spinner('Predicting...'):
      result = predict(selected_station, selected_date, selected_algorithm, 
                      #  selected_model
                       )
      rename_dict = dict(zip(result.columns, var_data["Description"]))
      result = result.rename(columns=rename_dict)
      result["Kelembapan rata-rata"] = result["Kelembapan rata-rata"] / 100
      result = result.reset_index()
      result = result.rename(columns = {"index":"Tanggal"})
      result['Tanggal'] = pd.to_datetime(result['Tanggal'])
      result['Tanggal'] = result['Tanggal'].dt.strftime("%d-%m-%Y")
      result = result.set_index('Tanggal')

      # st.dataframe(result.style.format({'Kelembapan rata-rata': '{:.2%}'}))

      st.dataframe(result.style.format(format_dict))
      # st.dataframe(result_df)

else:
  if disable_button:
    bool_button = False
  else:
    bool_button = bool(selected_station and selected_start_date and selected_end_date and selected_algorithm 
                      #  and selected_model
                       )

  predict_button = st.button("Predict", disabled= not bool_button)

  if predict_button:
    with st.spinner('Predicting...'):
      result = predict(selected_station, selected_end_date, selected_algorithm, 
                      #  selected_model, 
                       start_date=selected_start_date)

      img_df = result.copy()
      
      rename_dict = dict(zip(result.columns, var_data["Description"]))
      result = result.rename(columns=rename_dict)
      result["Kelembapan rata-rata"] = result["Kelembapan rata-rata"] / 100
      result = result.reset_index()
      result = result.rename(columns = {"index":"Tanggal"})
      result['Tanggal'] = pd.to_datetime(result['Tanggal'])
      result['Tanggal'] = result['Tanggal'].dt.strftime("%d-%m-%Y")
      result = result.set_index('Tanggal')

      st.dataframe(result.style.format(format_dict))

      # st.dataframe(result)
      if len(result) > 1:
        for col, unit in target_cols:
          plt.figure(figsize=(15, 5))
          plt.plot(img_df.index.to_numpy(), img_df[col].to_numpy(), label=col)
          plt.title(var_dict[col])
          plt.xlabel('Date')
          plt.ylabel('Values in ' + unit)
          # plt.legend(loc='upper right')
          plt.xticks(rotation=45)
          plt.grid(True)
          st.pyplot(plt)
