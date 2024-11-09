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
    # Search for a hotel and display relevant sentiment data and review text
st.header("Search for Hotel Sentiments")
hotel_name_input = st.text_input("Enter hotel name:", "")

if hotel_name_input:
    # Filter the summary data for the selected hotel
    selected_hotel_summary = hotel_sentiment_df[hotel_sentiment_df['hotel_name'].str.contains(hotel_name_input, case=False)]
    
    # Display sentiment scores and review text if the hotel is found in the summary data
    if not selected_hotel_summary.empty:
        st.subheader(f"Sentiment Scores for {hotel_name_input}")

        # Displaying the sentiment scores
        st.write(selected_hotel_summary[['avg_sentiment', 'food_score', 'service_score', 'staff_score', 
                                         'cleanliness_score', 'ambiance_score', 'value_score', 'room_score', 
                                         'amenities_score']])

        # Filtering review text from the individual reviews data for the selected hotel
        selected_hotel_reviews = review_details_df[review_details_df['hotel_name'].str.contains(hotel_name_input, case=False)]

        # Display individual review text if available
        if not selected_hotel_reviews.empty:
            st.subheader(f"Review Texts for {hotel_name_input}")
            st.write(selected_hotel_reviews[['Review Text']])
        else:
            st.write("No review text found for this hotel.")
    else:
        st.write("Hotel not found in summary data.")
