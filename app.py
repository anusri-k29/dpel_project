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

    # Load individual review details
    try:
        review_details_df = pd.read_csv('indi_reviews.csv')
    except FileNotFoundError:
        st.error("File 'indi_reviews.csv' not found. Please ensure it is in the app directory.")
        review_details_df = pd.DataFrame()  # Empty DataFrame as a fallback

    return hotel_sentiment_df, review_details_df

# Load data at the start of the app
hotel_sentiment_df, review_details_df = load_data()

# Display DataFrames if they loaded successfully (optional, for reference)
if not hotel_sentiment_df.empty:
    st.header("Aggregated Hotel Sentiment Summary")
    st.write(hotel_sentiment_df)

if not review_details_df.empty:
    st.header("Individual Review Details")
    st.write(review_details_df)

# Search for a hotel and display relevant sentiment data and review text
st.header("Search for Hotel Sentiments")

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

    # Display sentiment scores and review text if the hotel is found in the summary data
    if not selected_hotel_summary.empty:
        st.subheader(f"Sentiment Scores for {hotel_name_input}")

        # Displaying the sentiment scores
        st.write(selected_hotel_summary[['hotel_name', 'avg_sentiment', 'food_score', 'service_score', 'staff_score', 
                                         'cleanliness_score', 'ambiance_score', 'value_score', 'room_score', 
                                         'amenities_score']])

        # Display Overall Sentiment with color-coding
        overall_sentiment = selected_hotel_summary['Overall Sentiment'].values[0].lower()  # Getting overall sentiment

        # Color-coding based on sentiment value
        sentiment_colors = {
            'excellent': 'darkgreen',
            'good': 'lightgreen',
            'neutral': 'yellow',
            'bad': 'red'
        }
        
        # Display the overall sentiment with color
        overall_color = sentiment_colors.get(overall_sentiment, 'black')
        st.markdown(f"<h2 style='color:{overall_color};'>{overall_sentiment.capitalize()}</h2>", unsafe_allow_html=True)

        # Display category-wise sentiment with color coding
        st.subheader("Detailed Sentiments by Category")
        sentiment_categories = {
            'Food ': 'food_score',
            'Service ': 'service_score',
            'Staff ': 'staff_score',
            'Cleanliness ': 'cleanliness_score',
            'Ambiance ': 'ambiance_score',
            'Value ': 'value_score',
            'Room ': 'room_score',
            'Amenities ': 'amenities_score'
        }

        for category, score_col in sentiment_categories.items():
            # Get sentiment value and apply color
            category_sentiment = selected_hotel_summary[category].values[0].lower()
            category_color = sentiment_colors.get(category_sentiment, 'black')
            
            # Display category and sentiment with color
            st.markdown(f"<h3 style='color:{category_color};'>{category}: {category_sentiment.capitalize()}</h3>", unsafe_allow_html=True)
            
    else:
        st.write(f"Hotel '{hotel_name_input}' not found in the summary data.")
