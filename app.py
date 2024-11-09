import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data as usual
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

# Add a 'Month' and 'Year' column to review_details_df
if not review_details_df.empty:
    review_details_df['Stay Date'] = pd.to_datetime(review_details_df['Stay Date'], errors='coerce')  # Ensure the date is in datetime format
    review_details_df['Month'] = review_details_df['Stay Date'].dt.month
    review_details_df['Year'] = review_details_df['Stay Date'].dt.year

# User input for hotel name
hotel_name_input = st.text_input('Enter Hotel Name', '')

if hotel_name_input:
    # Filter reviews for the given hotel name
    filtered_reviews = review_details_df[review_details_df['hotel_name'].str.contains(hotel_name_input, case=False, na=False)]
    
    if not filtered_reviews.empty:
        # Group by Month and calculate review counts to show the popularity of months
        reviews_by_month = filtered_reviews.groupby('Month').size().reset_index(name='Review Count')
        
        # Sort by Month (Optional, but helpful for time-series)
        reviews_by_month = reviews_by_month.sort_values('Month')
        
        # Plot the data
        st.header(f"Popular Months for {hotel_name_input}")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Month', y='Review Count', data=reviews_by_month, ax=ax, palette='coolwarm')
        
        # Formatting
        ax.set_title(f"Most Popular Months for {hotel_name_input}", fontsize=16)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Number of Reviews", fontsize=12)
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
        
        # Show plot in Streamlit app
        st.pyplot(fig)
    else:
        st.warning(f"No reviews found for the hotel '{hotel_name_input}'. Please try a different hotel.")
