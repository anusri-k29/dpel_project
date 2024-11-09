import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

# Display DataFrames if they loaded successfully
if not hotel_sentiment_df.empty:
    st.header("Aggregated Hotel Sentiment Summary")
    st.write(hotel_sentiment_df)

if not review_details_df.empty:
    st.header("Individual Review Details")
    st.write(review_details_df)

# Hotel name search functionality
hotel_name = st.text_input('Enter the name of the hotel you want to analyze:')

# Check if the user inputted a hotel name
if hotel_name:
    # Filter reviews for the selected hotel
    hotel_reviews = review_details_df[review_details_df['hotel_name'].str.contains(hotel_name, case=False, na=False)]

    if not hotel_reviews.empty:
        st.write(f"Reviews for {hotel_name}:")
        
        # Ensure 'Stay Date' column is in DateTime format
        hotel_reviews['Stay Date'] = pd.to_datetime(hotel_reviews['Stay Date'], errors='coerce')

        # Extract Year and Month from 'Stay Date'
        hotel_reviews['Year'] = hotel_reviews['Stay Date'].dt.year
        hotel_reviews['Month'] = hotel_reviews['Stay Date'].dt.month_name()

        # List of categories to visualize
        categories = ['Food Quality Score', 'Service Quality Score', 'Staff Friendliness Score', 
                      'Cleanliness Score', 'Ambiance Score', 'Value for Money Score', 
                      'Room Comfort Score', 'Amenities Score']

        # Melt the data for monthly trends analysis
        category_trends = pd.melt(hotel_reviews, id_vars=['Year', 'Month'], value_vars=categories)

        # Group by Year, Month, and Category to get the average score
        category_trends_avg = category_trends.groupby(['Year', 'Month', 'variable'])['value'].mean().reset_index()

        # Plotting the results as a line plot
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=category_trends_avg, x='Month', y='value', hue='variable', marker='o')

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)

        # Show the plot
        st.pyplot(plt)
        
        # Display Overall Sentiment (Positive, Negative, Neutral, Excellent, Good, etc.)
        overall_sentiment = hotel_reviews['Sentiment'].mode()[0]  # Most frequent sentiment
        sentiment_color = {
            'Positive': 'green',
            'Negative': 'red',
            'Neutral': 'yellow',
            'Excellent': 'darkgreen',
            'Good': 'lightgreen',
            'Bad': 'red'
        }

        # Display the sentiment with the appropriate color
        st.markdown(f"### Overall Sentiment: <span style='color:{sentiment_color.get(overall_sentiment, 'black')};'>{overall_sentiment}</span>", unsafe_allow_html=True)

        # Display detailed sentiments for each category (Food, Staff, etc.)
        for category in categories:
            category_sentiment = hotel_reviews[f'{category} Sentiment'].mode()[0]  # Most frequent sentiment for each category
            st.markdown(f"**{category.replace('_', ' ').title()}:** <span style='color:{sentiment_color.get(category_sentiment, 'black')};'>{category_sentiment}</span>", unsafe_allow_html=True)

    else:
        st.write(f"No reviews found for {hotel_name}.")

else:
    st.write("Please enter a hotel name to start the analysis.")
