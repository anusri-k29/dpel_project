import streamlit as st
import pandas as pd

# Load data function with error handling
@st.cache_data
def load_data():
    # Load hotel sentiment summary
    try:
        hotel_sentiment_df = pd.read_csv('summary_review_1.csv')
    except FileNotFoundError:
        st.error("File 'summary_review_1.csv' not found. Please ensure it is in the app directory.")
        hotel_sentiment_df = pd.DataFrame()  # Empty DataFrame as a fallback

    return hotel_sentiment_df

# Load data at the start of the app
hotel_sentiment_df = load_data()

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

    # Display detailed sentiments by category if the hotel is found in the summary data
    if not selected_hotel_summary.empty:
        st.subheader("Detailed Sentiments by Category")
        
        # Color mapping based on sentiment value
        sentiment_colors = {
            'excellent': 'darkgreen',
            'good': 'lightgreen',
            'neutral': 'yellow',
            'bad': 'red'
        }

        # Define sentiment categories with column mappings
        sentiment_categories = {
            'Food Sentiment': 'Food Sentiment',
            'Service Sentiment': 'Service Sentiment',
            'Staff Sentiment': 'Staff Sentiment',
            'Cleanliness Sentiment': 'Cleanliness Sentiment',
            'Ambiance Sentiment': 'Ambiance Sentiment',
            'Value Sentiment': 'Value Sentiment',
            'Room Sentiment': 'Room Sentiment',
            'Amenities Sentiment': 'Amenities Sentiment'
        }

        # Display each category sentiment with color coding
        for category, score_col in sentiment_categories.items():
            # Get sentiment value and apply color
            category_sentiment = selected_hotel_summary[score_col].values[0].lower()
            category_color = sentiment_colors.get(category_sentiment, 'black')
            
            # Display category and sentiment with color
            st.markdown(f"<h3 style='color:{category_color};'>{category}: {category_sentiment.capitalize()}</h3>", unsafe_allow_html=True)
            
    else:
        st.write(f"Hotel '{hotel_name_input}' not found in the summary data.")
