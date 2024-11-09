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
# Search for a hotel
st.header("Search for Hotel Sentiments")
hotel_name_input = st.text_input("Enter hotel name:", "")

if hotel_name_input:
    # Filter the summary data for the selected hotel
    selected_hotel_summary = hotel_sentiment_df[hotel_sentiment_df['hotel_name'].str.contains(hotel_name_input, case=False)]
    
    # Display overall sentiment scores if the hotel is found in the summary data
    if not selected_hotel_summary.empty:
        st.subheader(f"Overall Sentiment Scores for {hotel_name_input}")
        st.write(selected_hotel_summary[['avg_sentiment', 'positive_reviews', 'neutral_reviews', 'negative_reviews']])

        st.write("### Specific Scores")
        st.write(selected_hotel_summary[['food_score', 'service_score', 'staff_score', 'cleanliness_score', 
                                         'ambiance_score', 'value_score', 'room_score', 'amenities_score']])
    else:
        st.write("Hotel not found in summary data.")

    # Filter individual review data for the selected hotel
    selected_hotel_reviews = review_details_df[review_details_df['hotel_name'].str.contains(hotel_name_input, case=False)]
    
    # Display individual review details for the hotel
    if not selected_hotel_reviews.empty:
        st.subheader(f"Individual Reviews for {hotel_name_input}")
        st.write(selected_hotel_reviews[['User Location', 'Rating', 'Review Title', 'Review Text', 
                                         'Food Quality Score', 'Service Quality Score', 'Staff Friendliness Score',
                                         'Cleanliness Score', 'Ambiance Score', 'Value for Money Score', 
                                         'Room Comfort Score', 'Amenities Score']])
    else:
        st.write("No individual reviews found for this hotel.")
