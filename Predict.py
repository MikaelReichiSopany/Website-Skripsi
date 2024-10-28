import streamlit as st
import joblib
import datetime
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from Dataset import init_connection, inv_station_dict, station_dict, var_dict, inv_var_dict, var_data


start_date_limit = datetime.date(2024, 7, 1)

def predict(station, date, model):
  chosen_station = db[str(inv_station_dict[station])]
  initial_data = chosen_station.find().sort({ 'Tanggal': -1 }).limit(7)
  loop_days = (date - start_date_limit).days

  if model == 'GRU':
    # load model and scaler
    model = joblib.load('GRU_Model/website_test_model.joblib')
    scaler = joblib.load('GRU_Model/scaler.joblib')

    # change mongodb object to df
    data_list = list(initial_data)
    data_df = pd.DataFrame(data_list)
    data_df = data_df.drop('_id',axis = 1 )
    data_df = data_df.iloc[::-1]
    data_df = data_df.set_index('Tanggal')

    # scale data
    scaled_data = scaler.transform(data_df)

    # predict using GRU model
    pred = model.predict(scaled_data)
    
    # return predictions to normal value
    inv_pred = scaler.inverse_transform(pred)

    pred_df = pd.DataFrame(inv_pred, columns=data_df)

    # # Iterative forecasting
    # predictions = []
    # for _ in range(forecast_horizon):
    #     # Make prediction
    #     pred = model.predict(scaled_data[-7:].reshape(1, 7, -1))  # Adjust shape as needed
    #     pred = scaler.inverse_transform(pred)

    #     # Append prediction to the data
    #     data_df = data_df.append(pd.DataFrame([[pred[0]]], index=[date + timedelta(days=1)], columns=data_df.columns), ignore_index=True)
    #     scaled_data = scaler.transform(data_df)
    #     date += timedelta(days=1)

    # return data_df[-forecast_horizon:]

  else:
    # load model
    model = joblib.load('RF_Model/website_test_model.joblib')

  return pred_df

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
    min_value=start_date_limit,
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

# if predict_button:
#    result = predict(selected_station, selected_date, selected_model, selected_var)
#    st.write(result)

if selected_station is not None:
  st.write("Available Variables:")
