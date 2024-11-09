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

####delete from this

import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('summary_review_1.csv')
    except FileNotFoundError:
        st.error("File 'summary_review_1.csv' not found. Please ensure it is in the app directory.")
        df = pd.DataFrame()  # Empty fallback
    return df

hotel_data = load_data()

# Initialize geolocator
geolocator = Nominatim(user_agent="hotel_locator")

# Function to get country coordinates
@st.cache_data
def get_country_coordinates(country):
    try:
        location = geolocator.geocode(country, timeout=10)
        return location.latitude, location.longitude if location else (None, None)
    except GeocoderTimedOut:
        return None, None

# Add coordinates to the DataFrame
hotel_data['coordinates'] = hotel_data['country'].apply(lambda x: get_country_coordinates(x) if pd.notna(x) else (None, None))
hotel_data[['latitude', 'longitude']] = pd.DataFrame(hotel_data['coordinates'].tolist(), index=hotel_data.index)

# Filter out rows without coordinates
hotel_data = hotel_data.dropna(subset=['latitude', 'longitude'])

# Display map if data is available
if not hotel_data.empty:
    st.title("Hotel Locations by Country")

    midpoint = (hotel_data['latitude'].mean(), hotel_data['longitude'].mean())
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=midpoint[0],
            longitude=midpoint[1],
            zoom=1,
            pitch=40,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=hotel_data,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=200000,
                pickable=True,
                auto_highlight=True,
            ),
        ],
        tooltip={"text": "{hotel_name} - {country}"},
    ))
else:
    st.write("Could not retrieve coordinates for any country in your dataset.")

