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
        if overall_sentiment == 'excellent':
            sentiment_color = 'darkgreen'
        elif overall_sentiment == 'good':
            sentiment_color = 'lightgreen'
        elif overall_sentiment == 'neutral':
            sentiment_color = 'yellow'
        elif overall_sentiment == 'bad':
            sentiment_color = 'red'
        else:
            sentiment_color = 'black'  # Default color if the sentiment is not recognized

        # Display the overall sentiment with color
        st.markdown(f"<h2 style='color:{sentiment_color};'>{overall_sentiment.capitalize()}</h2>", unsafe_allow_html=True)

        # Filtering review text from the individual reviews data for the selected hotel
        selected_hotel_reviews = review_details_df[review_details_df['hotel_name'].str.contains(hotel_name_input_cleaned, case=False)]

        # Display individual review text if available
        if not selected_hotel_reviews.empty:
            st.subheader(f"Review Texts for {hotel_name_input}")
            st.write(selected_hotel_reviews[['Review Text']])

            # Display the overall sentiment for each review with color-coding
            st.subheader(f"Sentiment for {hotel_name_input} Reviews")

            # Loop through the reviews and display sentiment with color coding
            for index, row in selected_hotel_reviews.iterrows():
                sentiment = row['Sentiment']
                
                # Apply color based on sentiment
                if sentiment.lower() == 'excellent':
                    sentiment_color = 'darkgreen'
                elif sentiment.lower() == 'good':
                    sentiment_color = 'lightgreen'
                elif sentiment.lower() == 'neutral':
                    sentiment_color = 'yellow'
                elif sentiment.lower() == 'bad':
                    sentiment_color = 'red'
                else:
                    sentiment_color = 'black'  # Default color for undefined sentiments

                # Display sentiment in big font with color
                st.markdown(f"<h3 style='color:{sentiment_color};'>{sentiment}</h3>", unsafe_allow_html=True)

        else:
            st.write("No review text found for this hotel.")
    else:
        st.write(f"Hotel '{hotel_name_input}' not found in the summary data.")
