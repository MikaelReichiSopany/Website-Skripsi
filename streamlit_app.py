import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = None

def login():
  st.session_state.logged_in = True
  st.rerun()

def logout():
  st.session_state.logged_in = False
  st.rerun()

# Define pages
predict_page = st.Page("Predict.py", title="Predict")
dataset_page = st.Page("Dataset.py", title="Dataset")
about_page = st.Page("About.py", title="About")
login_page = st.Page("Login.py", title="Login", default=True)
register_page = st.Page("Register.py", title="Register")

# Configure navigation with initial page selection
if st.session_state.logged_in:
  pg = st.navigation([predict_page, dataset_page, about_page])
else:
  pg = st.navigation([login_page, register_page])
  
pg.run()

