import streamlit as st
import joblib
import datetime
import numpy as np
import pandas as pd
from Dataset import init_connection, inv_station_dict, station_dict, var_dict, inv_var_dict, var_data


start_date_limit = datetime.date(2024, 6, 30)

def my_reshape (dataset, time_step):
  dataX = []
  a = dataset[0:(0 + time_step), :]
  dataX.append(a)
  return np.array(dataX)

def predict(station, date, model):


  time_step_gru = 14
  time_step_rf = 8

  chosen_station = db[str(inv_station_dict[station])]
  if model == 'GRU':
    initial_data = chosen_station.find().sort({ 'Tanggal': -1 }).limit(time_step_gru)
  else:
    initial_data = chosen_station.find().sort({ 'Tanggal': -1 }).limit(time_step_rf)
  loop_days = (date - start_date_limit).days

# change mongodb object to df
  data_list = list(initial_data)
  data_df = pd.DataFrame(data_list)
  data_df = data_df.drop('_id',axis = 1 )
  data_df = data_df.iloc[::-1]
  data_df = data_df.set_index('Tanggal')

  if model == 'GRU':
    # load model and scaler
    model = joblib.load('GRU_Model/gru_model.joblib')
    scaler = joblib.load('GRU_Model/scaler.joblib')

    # # change mongodb object to df
    # data_list = list(initial_data)
    # data_df = pd.DataFrame(data_list)
    # data_df = data_df.drop('_id',axis = 1 )
    # data_df = data_df.iloc[::-1]
    # data_df = data_df.set_index('Tanggal')

    # # scale data
    scaled_data = scaler.transform(data_df)
    scaled_data = my_reshape(scaled_data, time_step_gru)

    # # predict using GRU model
    # pred = model.predict(scaled_data)

    # # return predictions to normal value
    # inv_pred = scaler.inverse_transform(pred)

    # pred_df = pd.DataFrame(inv_pred)

    # pred_df.columns = data_df.columns
    # pred_df.insert(0, 'Tanggal', date)

    # # Iterative forecasting
    date_for_index = start_date_limit
    for _ in range(loop_days):
        
        date_for_index += datetime.timedelta(days=1)

        # Make prediction
        pred = model.predict(scaled_data[-time_step_gru:].reshape(1, time_step_gru, -1))  # Adjust shape as needed
        pred = scaler.inverse_transform(pred)

        pred_df = pd.DataFrame(pred)
        pred_df.index = [date_for_index]
        pred_df.columns = data_df.columns

        data_df = pd.concat([data_df, pred_df])
        scaled_data = scaler.transform(data_df)

    return data_df[-loop_days:]

  else:
    # load model
    date_for_index = start_date_limit
    for _ in range(loop_days):
      
      date_for_index += datetime.timedelta(days=1)
      all_var_pred = []

      for var, desc in  var_dict.items():
        model = joblib.load(f'RF_Model/{var}.joblib')
        prep_data = my_reshape(data_df[-time_step_rf:].values, time_step_rf)

        pred = model.predict(prep_data.reshape(prep_data.shape[0], -1))
        all_var_pred.append(pred[0])

      pred_df = pd.DataFrame(all_var_pred)
      pred_df = pred_df.transpose()
      pred_df.columns = data_df.columns
      pred_df.insert(0, 'Tanggal', date_for_index)

      pred_df = pred_df.set_index('Tanggal')

      data_df = pd.concat([data_df, pred_df])

    return data_df[-loop_days:]

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

selected_date = st.date_input(
    "Select a Date",
    value=None,
    format = "DD/MM/YYYY",
    min_value=start_date_limit + datetime.timedelta(days=1),
    key = 'date'
)

selected_model = st.selectbox(
    "Select a Model",
    ["GRU", "Random Forest"],
    index=None,
    placeholder="Select a Model",
    key='model'
)

# if selected_model is not None:

#   st.write("Select Variable to Predict")

#   var_list = list(var_dict.values())
#   selected_var = []

#   for var in var_list:
#       selected = st.checkbox(var)
#       if selected:
#           selected_var.append(var)

bool_button = bool(selected_station and selected_date and selected_model)

predict_button = st.button("Predict", disabled= not bool_button)

if predict_button:
  #  result = predict(selected_station, selected_date, selected_model, selected_var)
  with st.spinner('Predicting...'):
    result = predict(selected_station, selected_date, selected_model)
    st.success('Predicting Success')
    #  st.write(result)
    st.dataframe(result)


# if selected_station is not None:
#   st.write("Available Variables:")
