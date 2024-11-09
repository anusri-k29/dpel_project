import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data function with error handling
@st.cache_data
def load_data():
    try:
        hotel_sentiment_df = pd.read_csv('summary_review_1.csv')
        review_details_df = pd.read_csv('indi_reviews.csv')
    except FileNotFoundError:
        st.error("One or more required files are missing.")
        return pd.DataFrame(), pd.DataFrame()

    return hotel_sentiment_df, review_details_df

# Load data
hotel_sentiment_df, review_details_df = load_data()

# Search for a hotel and display relevant sentiment data
st.header("Search for Hotel Sentiments by Category")

# Input field for the hotel name
hotel_name_input = st.text_input("Enter hotel name:")

# Add a button to trigger the search
search_button = st.button("Search Hotel Sentiment")

if search_button and hotel_name_input:
    # Clean up the hotel name input (strip spaces and convert to lowercase for case-insensitive matching)
    hotel_name_input_cleaned = hotel_name_input.strip().lower()

    # Remove leading/trailing spaces and handle NaN values in the hotel_name column
    hotel_sentiment_df['hotel_name_cleaned'] = hotel_sentiment_df['hotel_name'].str.strip().str.lower()

    # Filter the summary data for the selected hotel based on cleaned name
    selected_hotel_summary = hotel_sentiment_df[hotel_sentiment_df['hotel_name_cleaned'].str.contains(hotel_name_input_cleaned)]

    # Display overall sentiment and detailed sentiments by category if the hotel is found in the summary data
    if not selected_hotel_summary.empty:
        
        # Color mapping based on sentiment value
        sentiment_colors = {
            'excellent': 'darkgreen',
            'good': 'lightgreen',
            'neutral': 'yellow',
            'bad': 'red'
        }

        # Get and display the overall sentiment
        overall_sentiment = selected_hotel_summary['Overall Sentiment'].values[0].lower()
        overall_color = sentiment_colors.get(overall_sentiment, 'black')
        st.markdown(f"<h2 style='color:{overall_color};'>Overall Sentiment: {overall_sentiment.capitalize()}</h2>", unsafe_allow_html=True)

        # Display detailed sentiments by category in a compact format
        st.subheader("Detailed Sentiments by Category")
        
        # Define sentiment categories with column mappings
        sentiment_categories = {
            'Food': 'Food Sentiment',
            'Service': 'Service Sentiment',
            'Staff': 'Staff Sentiment',
            'Cleanliness': 'Cleanliness Sentiment',
            'Ambiance': 'Ambiance Sentiment',
            'Value': 'Value Sentiment',
            'Room': 'Room Sentiment',
            'Amenities': 'Amenities Sentiment'
        }

        # Arrange the sentiments into columns for a compact display
        col1, col2 = st.columns(2)

        for idx, (category, score_col) in enumerate(sentiment_categories.items()):
            # Get sentiment value and apply color
            category_sentiment = selected_hotel_summary[score_col].values[0].lower()
            category_color = sentiment_colors.get(category_sentiment, 'black')
            sentiment_display = f"{category}: {category_sentiment.capitalize()}"

            # Display in alternating columns
            if idx % 2 == 0:
                col1.markdown(f"<p style='color:{category_color}; font-size:18px;'>{sentiment_display}</p>", unsafe_allow_html=True)
            else:
                col2.markdown(f"<p style='color:{category_color}; font-size:18px;'>{sentiment_display}</p>", unsafe_allow_html=True)

    else:
        st.write(f"Hotel '{hotel_name_input}' not found in the summary data.")

# Add a 'Month' and 'Year' column to review_details_df for time-based analysis
if not review_details_df.empty:
    review_details_df['Stay Date'] = pd.to_datetime(review_details_df['Stay Date'], errors='coerce')  # Ensure the date is in datetime format
    review_details_df['Month'] = review_details_df['Stay Date'].dt.month_name()
    review_details_df['Year'] = review_details_df['Stay Date'].dt.year
if not review_details_df.empty:
    review_details_df['Stay Date'] = pd.to_datetime(review_details_df['Stay Date'], errors='coerce')  # Ensure the date is in datetime format
    review_details_df['Month'] = review_details_df['Stay Date'].dt.month_name()
    review_details_df['Year'] = review_details_df['Stay Date'].dt.year

# Plotting the count of reviews by Month for the selected hotel
if hotel_name_input and not review_details_df.empty:
    hotel_reviews = review_details_df[review_details_df['hotel_name'].str.contains(hotel_name_input, case=False, na=False)]
    
    if not hotel_reviews.empty:
        st.subheader(f"Most Popular Time to Visit {hotel_name_input}")
        
        # Plotting the count of reviews by Month
        plt.figure(figsize=(10, 6))
        sns.countplot(data=hotel_reviews, x='Month', palette='viridis')

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)

        # Show the plot
        st.pyplot(plt)
    else:
        st.write(f"No reviews found for {hotel_name_input}.")
# Filter reviews by hotel_name_input
hotel_reviews = review_details_df[review_details_df['hotel_name'].str.contains(hotel_name_input, case=False, na=False)]

# Top Positive & Negative Reviews
if hotel_name_input and not hotel_reviews.empty:
    hotel_reviews_sorted_by_sentiment = hotel_reviews.sort_values(by='Sentiment Score', ascending=False)
    
    if not hotel_reviews_sorted_by_sentiment.empty:
        st.subheader(f"Top Positive Review for {hotel_name_input}")
        top_positive_review = hotel_reviews_sorted_by_sentiment.iloc[0]
        st.write(f"**Rating:** {top_positive_review['Rating']}")
        st.write(f"**Review Title:** {top_positive_review['Review Title']}")
        st.write(f"**Review Text:** {top_positive_review['Review Text']}")
        
        st.subheader(f"Top Negative Review for {hotel_name_input}")
        top_negative_review = hotel_reviews_sorted_by_sentiment.iloc[-1]
        st.write(f"**Rating:** {top_negative_review['Rating']}")
        st.write(f"**Review Title:** {top_negative_review['Review Title']}")
        st.write(f"**Review Text:** {top_negative_review['Review Text']}")
    else:
        st.write(f"No reviews available for {hotel_name_input}.")
import numpy as np
from math import pi

# Part 1: Types of Travelers (Pie Chart)
st.subheader("Types of Travelers")
# Check if data includes traveler type column
if 'Traveler Type' in review_details_df.columns:
    traveler_counts = review_details_df['Traveler Type'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(traveler_counts, labels=traveler_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2"))
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)
else:
    st.write("Traveler Type information not available.")
    st.subheader("Top 5 Hotels by Sentiment Score")
top_hotels = hotel_sentiment_df.nlargest(5, 'avg_sentiment')
st.table(top_hotels[['hotel_name', 'avg_sentiment']])
