import streamlit as st
import pandas as pd

import pymongo

import bcrypt
import streamlit_app


@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

db = client["Skripsi"]
collection = db['USER']


def hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def register_account(username, name, email, password):
    result_username = collection.find_one({"username": username })
    result_email = collection.find_one({"email": email })

    if result_username is None and result_email is None:
      users = {
        'username':username,
        'password': hash(password),
        'email': email,
        'name': name
      }
      collection.insert_one(users)
      st.success('Account registered successfully, please Login')
    else:
        st.warning("Username or email already registered")

st.subheader('Register')
username = st.text_input('Username')
name = st.text_input('Full Name')
email = st.text_input('Email')
password = st.text_input('Password', type='password')
confirm_password = st.text_input('Confirm Password', type='password')

if password != confirm_password:
    st.error('Password does not match')

disable_button = True

if username and name and email and password and password == confirm_password:
    disable_button = False

submit_button = st.button('Register', on_click=register_account, args=(username, name, email, password), disabled=disable_button)


# login_button = st.page_link(st.Page("Login.py", title="Login"), label='Already have an account ?')

