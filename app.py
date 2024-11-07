import streamlit as st
import pandas as pd

# Title of the app
st.title('Hotel Review Sentiment Analysis')

# Sidebar for navigation
st.sidebar.title('Navigation')
app_mode = st.sidebar.radio("Choose an option", ["Home", "Hotel Sentiment", "Review Details"])

# Home Page
if app_mode == "Home":
    st.header("Welcome to the Hotel Review Sentiment Analysis App!")
    st.write(
        """
        This app allows you to visualize sentiment analysis results for hotel reviews. 
        You can explore individual review data and aggregated sentiment scores per hotel.
        """
    )

# Hotel Sentiment Page
elif app_mode == "Hotel Sentiment":
    st.header("Aggregated Hotel Sentiment Summary")

    # Load the CSV file with hotel sentiment data
    try:
        hotel_sentiment_df = pd.read_csv('summary4.csv')  # Make sure your path is correct
        st.write(hotel_sentiment_df)
    except FileNotFoundError:
        st.error("The 'summary4.csv' file is not found. Please check the path.")

# Review Details Page
elif app_mode == "Review Details":
    st.header("Individual Review Details")

    # Load the individual review CSV file
    try:
        review_details_df = pd.read_csv('indi4.csv')  # Make sure your path is correct
        st.write(review_details_df)
    except FileNotFoundError:
        st.error("The 'indi4.csv' file is not found. Please check the path.")
