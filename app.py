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
# Rating vs Sentiment Heatmap
if hotel_name_input and not review_details_df.empty:
    hotel_reviews = review_details_df[review_details_df['hotel_name'].str.contains(hotel_name_input, case=False, na=False)]
    
    if not hotel_reviews.empty:
        # Sentiment columns from summary_review_1.csv
        sentiment_columns = [
            'Food Sentiment', 'Service Sentiment', 'Staff Sentiment', 
            'Cleanliness Sentiment', 'Ambiance Sentiment', 'Value Sentiment', 
            'Room Sentiment', 'Amenities Sentiment'
        ]

        # Check if all sentiment columns exist in the hotel_sentiment_df
        missing_columns = [col for col in sentiment_columns if col not in hotel_sentiment_df.columns]
        if missing_columns:
            st.error(f"Missing sentiment columns: {missing_columns}")
        else:
            # Mapping sentiments to numerical values
            sentiment_mapping = {
                'excellent': 4,
                'good': 3,
                'neutral': 2,
                'bad': 1
            }

            # Apply sentiment mapping to convert sentiments to numeric values in hotel_sentiment_df
            for col in sentiment_columns:
                hotel_sentiment_df[col] = hotel_sentiment_df[col].map(sentiment_mapping)

            # Merge hotel_reviews with sentiment data from hotel_sentiment_df
            merged_df = pd.merge(hotel_reviews, hotel_sentiment_df[['hotel_name'] + sentiment_columns], on='hotel_name', how='inner')

            # Create a DataFrame with Rating and sentiment columns for correlation
            rating_sentiment_df = merged_df[['Rating'] + sentiment_columns].dropna()

            # Calculate the correlation matrix
            correlation_matrix = rating_sentiment_df.corr()

            # Plot the heatmap
            plt.figure(figsize=(10, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
            plt.title(f"Rating vs Sentiment Correlation for {hotel_name_input}")
            st.pyplot(plt)
    else:
        st.write(f"No reviews found for {hotel_name_input}.")

# Top Positive & Negative Reviews
if hotel_name_input and not review_details_df.empty:
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
