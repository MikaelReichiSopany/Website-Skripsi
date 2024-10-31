import streamlit as st
import joblib
import datetime
import numpy as np
import pandas as pd
import pymongo
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


inv_station_dict = {
    "Stasiun Klimatologi Sumatera Selatan": "SK_SUMSEL",
    "Stasiun Klimatologi Sumatera Utara": "SK_SUMUT",
    "Stasiun Meteorologi Binaka": "SM_BINAKA",
    "Stasiun Meteorologi Kualanamu": "SM_KUALANAMU",
    "Stasiun Meteorologi Minangkabau": "SM_MINANGKABAU",
    "Stasiun Meteorologi Sultan Mahmud Badaruddin II": "SM_SULTAN",
    "Stasiun Meteorologi FL Tobing": "SM_TOBING"
}

station_dict = {
    "SK_SUMSEL": "Stasiun Klimatologi Sumatera Selatan",
    "SK_SUMUT": "Stasiun Klimatologi Sumatera Utara",
    "SM_BINAKA": "Stasiun Meteorologi Binaka",
    "SM_KUALANAMU": "Stasiun Meteorologi Kualanamu",
    "SM_MINANGKABAU": "Stasiun Meteorologi Minangkabau",
    "SM_SULTAN": "Stasiun Meteorologi Sultan Mahmud Badaruddin II",
    "SM_TOBING": "Stasiun Meteorologi FL Tobing"
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

def predict(station, date, algorithm, model_number, start_date = None):

  # uwu
  # if model_number < 5:
  #   time_step = 7
  # else:
  #   time_step = 14

  if algorithm == 'GRU':
    time_step = 14
  else:
    time_step = 8

  chosen_station = db[str(inv_station_dict[station])]

  initial_data = chosen_station.find().sort({ 'Tanggal': -1 }).limit(time_step)

  loop_days = (date - start_date_limit).days

# change mongodb object to df
  data_list = list(initial_data)
  data_df = pd.DataFrame(data_list)
  data_df = data_df.drop('_id',axis = 1 )
  data_df = data_df.iloc[::-1]
  data_df = data_df.set_index('Tanggal')

  if algorithm == 'GRU':
    # load model and scaler
    # uwu
    # model = joblib.load(f'GRU_Model/gru_{model_number}.joblib')
    model = joblib.load(f'GRU_Model/gru_model.joblib')
    scaler = joblib.load(f'GRU_Model/scaler.joblib')

    # # scale data
    scaled_data = scaler.transform(data_df)
    scaled_data = my_reshape(scaled_data, time_step)

    # # Iterative forecasting
    date_for_index = start_date_limit
    for _ in range(loop_days):
        
        date_for_index += datetime.timedelta(days=1)

        # Make prediction
        pred = model.predict(scaled_data[-time_step:].reshape(1, time_step, -1))  # Adjust shape as needed
        pred = scaler.inverse_transform(pred)

        pred_df = pd.DataFrame(pred)
        pred_df.index = [date_for_index]
        pred_df.columns = data_df.columns

        data_df = pd.concat([data_df, pred_df])
        scaled_data = scaler.transform(data_df)

    # if start_date:
    #   range_day = (date - start_date).days
    #   return data_df[-(range_day + 1):]
    # else:
    #   return data_df[-1:]

  else:
    # load model
    date_for_index = start_date_limit
    for _ in range(loop_days):
      
      date_for_index += datetime.timedelta(days=1)
      all_var_pred = []

      for var, desc in  var_dict.items():
        # uwu
        # model = joblib.load(f'RF_Model/{model_number}_{var}.joblib')
        model = joblib.load(f'RF_Model/{var}.joblib')
        prep_data = my_reshape(data_df[-time_step:].values, time_step)

        pred = model.predict(prep_data.reshape(prep_data.shape[0], -1))
        all_var_pred.append(pred[0])

      pred_df = pd.DataFrame(all_var_pred)
      pred_df = pred_df.transpose()
      pred_df.columns = data_df.columns
      pred_df.insert(0, 'Tanggal', date_for_index)

      pred_df = pred_df.set_index('Tanggal')

      data_df = pd.concat([data_df, pred_df])

    # return data_df[-loop_days:]
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
      st.error("Selected End Date must be more than Selected Start Date")

selected_algorithm = st.selectbox(
    "Select a algorithm",
    ["GRU", "Random Forest"],
    index=None,
    placeholder="Select a algorithm",
    key='algorithm'
)

selected_model = st.selectbox(
  "Select a Model",
  ['1', '2', '3', '4', '5', '6', '7', '8'],
  index=None,
  placeholder="Select a algorithm",
  key='model'
)



if not date_toggle:
  bool_button = bool(selected_station and selected_date and selected_algorithm and selected_model)

  predict_button = st.button("Predict", disabled= not bool_button)

  if predict_button:
    with st.spinner('Predicting...'):
      result = predict(selected_station, selected_date, selected_algorithm, selected_model)

      st.dataframe(result)

else:
  bool_button = bool(selected_station and selected_start_date and selected_end_date and selected_algorithm and selected_model)

  predict_button = st.button("Predict", disabled= not bool_button)

  if predict_button:
    with st.spinner('Predicting...'):
      result = predict(selected_station, selected_end_date, selected_algorithm, selected_model, start_date=selected_start_date)

      st.dataframe(result)
      if len(result) > 1:
        for col, unit in target_cols:
          plt.figure(figsize=(15, 5))
          plt.plot(result.index.to_numpy(), result[col].to_numpy(), label=col)
          plt.title(var_dict[col] + f' ({col})')
          plt.xlabel('Date')
          plt.ylabel('Values in ' + unit)
          plt.legend(loc='upper right')
          plt.xticks(rotation=45)
          plt.grid(True)
          st.pyplot(plt)
