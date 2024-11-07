import streamlit as st
import pandas as pd

# Title of the app
st.title('Hotel Review Sentiment Analysis')

# Display a short description
st.write("""
    This app allows you to upload and view hotel sentiment data and individual review details.
    You can upload the CSV files for 'Hotel Sentiment Summary' and 'Individual Reviews' and see the analysis results.
""")

# File uploader for 'Hotel Sentiment Summary'
st.header("Aggregated Hotel Sentiment Summary")
uploaded_summary_file = st.file_uploader("Upload Hotel Sentiment CSV", type=["csv"])
if uploaded_summary_file is not None:
    hotel_sentiment_df = pd.read_csv(uploaded_summary_file)
    st.write(hotel_sentiment_df)
else:
    st.write("Please upload the 'summary4.csv' file to see aggregated hotel sentiment data.")

# File uploader for 'Individual Review Details'
st.header("Individual Review Details")
uploaded_reviews_file = st.file_uploader("Upload Review Details CSV", type=["csv"])
if uploaded_reviews_file is not None:
    review_details_df = pd.read_csv(uploaded_reviews_file)
    st.write(review_details_df)
else:
    st.write("Please upload the 'indi4.csv' file to see the individual review details.")
