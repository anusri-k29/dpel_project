import streamlit as st
import pandas as pd
import os

# Load data function with error handling
@st.cache_data
def load_data():
    # Load hotel sentiment summary
    try:
        hotel_sentiment_df = pd.read_csv('summarynew4.csv')
    except FileNotFoundError:
        st.error("File 'summarynew4.csv' not found. Please ensure it is in the app directory.")
        hotel_sentiment_df = pd.DataFrame()  # Empty DataFrame as a fallback

    # Load individual review details
    try:
        review_details_df = pd.read_csv('indinew4 (1).csv')
    except FileNotFoundError:
        st.error("File 'indinew4 (1).csv' not found. Please ensure it is in the app directory.")
        review_details_df = pd.DataFrame()  # Empty DataFrame as a fallback

    # Load unique hotels data
    try:
        unique_hotels_df = pd.read_csv('unique_hotels1.csv')
    except FileNotFoundError:
        st.error("File 'unique_hotels1.csv' not found. Please ensure it is in the app directory.")
        unique_hotels_df = pd.DataFrame()  # Empty DataFrame as a fallback

    # Load all reviews data
    try:
        all_reviews_df = pd.read_csv('all_reviews.csv')
    except FileNotFoundError:
        st.error("File 'all_reviews.csv' not found. Please ensure it is in the app directory.")
        all_reviews_df = pd.DataFrame()  # Empty DataFrame as a fallback

    return hotel_sentiment_df, review_details_df, unique_hotels_df, all_reviews_df

# Load data at the start of the app
hotel_sentiment_df, review_details_df, unique_hotels_df, all_reviews_df = load_data()

# Display DataFrames if they loaded successfully
if not hotel_sentiment_df.empty:
    st.header("Aggregated Hotel Sentiment Summary")
    st.write(hotel_sentiment_df)

if not review_details_df.empty:
    st.header("Individual Review Details")
    st.write(review_details_df)

if not unique_hotels_df.empty:
    st.header("Unique Hotels")
    st.write(unique_hotels_df)

if not all_reviews_df.empty:
    st.header("All Reviews")
    st.write(all_reviews_df)
