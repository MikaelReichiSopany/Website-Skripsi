import streamlit as st

# Define pages
predict_page = st.Page("Predict.py", title="Predict", default=True)
dataset_page = st.Page("Dataset.py", title="Dataset")
about_page = st.Page("About.py", title="About")

# Configure navigation with initial page selection
pg = st.navigation([predict_page, dataset_page, about_page])

# Run the selected page
pg.run()