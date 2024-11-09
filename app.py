
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Title of the app
st.title('Hotel Review Sentiment Analysis')

# Display a short description
st.write("""
    This app displays hotel sentiment data and individual review details.
    View the preloaded datasets for the 'Hotel Sentiment Summary' and 'Individual Reviews' along with analysis results.
""")

# Load the CSV files directly
@st.cache
def load_data():
    hotel_sentiment_df = pd.read_csv('summary4.csv')  # Ensure this file is in the same directory
    review_details_df = pd.read_csv('indi4.csv')      # Ensure this file is in the same directory
    return hotel_sentiment_df, review_details_df

hotel_sentiment_df, review_details_df = load_data()

# Display Aggregated Hotel Sentiment Summary
st.header("Aggregated Hotel Sentiment Summary")
st.write(hotel_sentiment_df)

# Visualize the distribution of sentiments
st.subheader("Sentiment Distribution")
sentiment_counts = hotel_sentiment_df['Sentiment'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax, palette="Set2")
ax.set_xlabel("Sentiment")
ax.set_ylabel("Count")
st.pyplot(fig)

# Display Individual Review Details
st.header("Individual Review Details")
st.write(review_details_df)

# Filter reviews by sentiment
st.subheader("Filter Reviews by Sentiment")
sentiment_filter = st.selectbox("Select sentiment to filter reviews", ["All", "Positive", "Neutral", "Negative"])

if sentiment_filter != "All":
    filtered_reviews = review_details_df[review_details_df['Sentiment'] == sentiment_filter]
    st.write(filtered_reviews)
else:
    st.write(review_details_df)

# Optional: Display a word cloud for the filtered sentiment
if sentiment_filter != "All":
    st.subheader(f"Word Cloud for {sentiment_filter} Reviews")
    words = " ".join(review for review in filtered_reviews['Review'])
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(words)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)
