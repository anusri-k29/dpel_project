import streamlit as st
import pandas as pd

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
        st.subheader("Overall Sentiment")
        
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

# Add a 'Month' and 'Year' column to review_details_df
if not review_details_df.empty:
    review_details_df['Stay Date'] = pd.to_datetime(review_details_df['Stay Date'], errors='coerce')  # Ensure the date is in datetime format
    review_details_df['Month'] = review_details_df['Stay Date'].dt.month
    review_details_df['Year'] = review_details_df['Stay Date'].dt.year

# 1. Monthly Review Volume Analysis
st.header('Monthly Review Volume Analysis')
if not review_details_df.empty:
    reviews_by_month = review_details_df.groupby(['Year', 'Month']).size().reset_index(name='Review Count')
    fig, ax = plt.subplots()
    sns.lineplot(x='Month', y='Review Count', hue='Year', data=reviews_by_month, marker='o', ax=ax)
    ax.set_title("Number of Reviews by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Reviews")
    st.pyplot(fig)

# 2. Sentiment by Month
st.header('Sentiment by Month')
if not review_details_df.empty:
    # Convert Sentiment column to numeric scores (assuming positive = 1, neutral = 0, negative = -1)
    sentiment_map = {'positive': 1, 'neutral': 0, 'negative': -1}
    review_details_df['Sentiment Score'] = review_details_df['Sentiment'].map(sentiment_map)

    # Group by month and year to calculate average sentiment score
    sentiment_by_month = review_details_df.groupby(['Year', 'Month'])['Sentiment Score'].mean().reset_index(name='Average Sentiment')

    fig, ax = plt.subplots()
    sns.lineplot(x='Month', y='Average Sentiment', hue='Year', data=sentiment_by_month, marker='o', ax=ax)
    ax.set_title("Average Sentiment by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average Sentiment")
    st.pyplot(fig)

# 3. Seasonal Sentiment Trends by Category (e.g., Food, Service, Cleanliness)
st.header('Seasonal Sentiment Trends by Category')
if not review_details_df.empty:
    categories = ['Food Quality Score', 'Service Quality Score', 'Staff Friendliness Score', 
                  'Cleanliness Score', 'Ambiance Score', 'Value for Money Score', 'Room Comfort Score', 'Amenities Scores']
    
    # Prepare data for each category to analyze its trend over months
    category_trends = pd.melt(review_details_df, id_vars=['Year', 'Month'], value_vars=categories,
                              var_name='Category', value_name='Score')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='Month', y='Score', hue='Category', data=category_trends, marker='o', ax=ax)
    ax.set_title("Seasonal Sentiment Trends by Category")
    ax.set_xlabel("Month")
    ax.set_ylabel("Score")
    st.pyplot(fig)
