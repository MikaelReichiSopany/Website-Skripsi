import streamlit as st
import pandas as pd

import pymongo

import bcrypt
import streamlit_app
# from Dataset import init_connection

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

db = client["Skripsi"]
collection = db['USER']


def check_pw(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def authenticate(username, password):
    
    result = collection.find_one({"username": username })

    st.session_state["authentication_status"] = False

    if result:
      if check_pw(password, result['password']):
        st.session_state["username"] = result['username']
        st.session_state["authentication_status"] = True
        st.session_state["name"] = result['name']

# login_form = st.form(key='Login', clear_on_submit=False, enter_to_submit=False)

# with st.form(key='Login', clear_on_submit=False, enter_to_submit=False):

st.subheader('Login')
username = st.text_input('Username')
password = st.text_input('Password', type='password')

submit_button = st.button('Login', on_click=authenticate, args=(username, password))

# register_button = st.page_link(st.Page("Register.py", title="Register"), label='Register')

if st.session_state["authentication_status"]:
  streamlit_app.login()
  pass

elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
# st.session_state
