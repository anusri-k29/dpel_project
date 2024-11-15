import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Sidebar for page selection
page = st.sidebar.selectbox("Choose a Page", ["SSCA Data Analysis", "Hotel Sentiment Analysis"])

# File uploader for SSCA and Hotel Data
st.sidebar.title("Upload Required Files")
if page == "SSCA Data Analysis":
    ssca_file = st.sidebar.file_uploader("Upload SSCA Data (CSV)", type="csv")

if page == "Hotel Sentiment Analysis":
    hotel_sentiment_file = st.sidebar.file_uploader("Upload Hotel Sentiment Data (CSV)", type="csv", key="sentiment")
    review_details_file = st.sidebar.file_uploader("Upload Review Details Data (CSV)", type="csv", key="review_details")
    all_reviews_file = st.sidebar.file_uploader("Upload All Reviews Data (CSV)", type="csv", key="all_reviews")

# ----------------SSCA Data Analysis Page----------------------------
if page == "SSCA Data Analysis":
    if ssca_file is not None:
        data = pd.read_csv(ssca_file)
        st.title("SSCA Data Analysis Dashboard")
        st.write("An interactive dashboard providing insights and visualizations on SSCA data.")

        # Display SSCA data table
        st.subheader("SSCA Dataset")
        st.dataframe(data)

        # Age Distribution
        st.subheader("Age Distribution")
        fig, ax = plt.subplots()
        sns.histplot(data['Age'], bins=10, kde=True, ax=ax)
        ax.set_title("Age Distribution")
        ax.set_xlabel("Age")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        # Gender Distribution across Culinary Specializations
        st.subheader("Gender Distribution Across Culinary Specializations")
        fig, ax = plt.subplots()
        sns.countplot(data=data, x='CAdept', hue='Gender', ax=ax)
        ax.set_title("Gender Distribution across Culinary Specializations")
        ax.set_xlabel("Culinary Department")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Filter by Age Range
        st.subheader("Filter by Age Range")
        age_range = st.slider("Select Age Range", int(data['Age'].min()), int(data['Age'].max()), (18, 24))
        filtered_data = data[(data['Age'] >= age_range[0]) & (data['Age'] <= age_range[1])]
        st.write(f"Data for Age Range {age_range[0]} - {age_range[1]}")
        st.dataframe(filtered_data)
    else:
        st.warning("Please upload the SSCA data file to proceed.")

# ----------------Hotel Sentiment Analysis Page-----------------------
if page == "Hotel Sentiment Analysis":
    if hotel_sentiment_file and review_details_file and all_reviews_file:
        # Load data
        hotel_sentiment_df = pd.read_csv(hotel_sentiment_file)
        review_details_df = pd.read_csv(review_details_file)
        all_reviews_df = pd.read_csv(all_reviews_file)

        st.title("Hotel Sentiment Analysis Dashboard")
        st.write("Search and explore sentiment analysis by hotel.")

        # Input field for hotel name and search button
        hotel_name_input = st.text_input("Enter hotel name:")
        search_button = st.button("Search Hotel Sentiment")
        if search_button and hotel_name_input:
            hotel_name_input_cleaned = hotel_name_input.strip().lower()
            hotel_sentiment_df['hotel_name_cleaned'] = hotel_sentiment_df['hotel_name'].str.strip().str.lower()
            selected_hotel_summary = hotel_sentiment_df[hotel_sentiment_df['hotel_name_cleaned'].str.contains(hotel_name_input_cleaned)]

            if not selected_hotel_summary.empty:
                # Define colors for different sentiment levels
                sentiment_colors = {'excellent': 'darkgreen', 'good': 'lightgreen', 'neutral': 'yellow', 'bad': 'red'}
                overall_sentiment = selected_hotel_summary['Overall Sentiment'].values[0].lower()
                overall_color = sentiment_colors.get(overall_sentiment, 'black')
                st.markdown(f"<h2 style='color:{overall_color};'>Overall Sentiment: {overall_sentiment.capitalize()}</h2>", unsafe_allow_html=True)

                # Display detailed sentiments by category
                st.subheader("Detailed Sentiments by Category")
                sentiment_categories = {
                    'Food': 'Food Sentiment', 'Service': 'Service Sentiment', 'Staff': 'Staff Sentiment',
                    'Cleanliness': 'Cleanliness Sentiment', 'Ambiance': 'Ambiance Sentiment',
                    'Value': 'Value Sentiment', 'Room': 'Room Sentiment', 'Amenities': 'Amenities Sentiment'
                }
                # Display categories in two columns
                col1, col2 = st.columns(2)
                for idx, (category, score_col) in enumerate(sentiment_categories.items()):
                    category_sentiment = selected_hotel_summary[score_col].values[0].lower()
                    category_color = sentiment_colors.get(category_sentiment, 'black')
                    sentiment_display = f"{category}: {category_sentiment.capitalize()}"

                    if idx % 2 == 0:
                        col1.markdown(f"<p style='color:{category_color}; font-size:18px;'>{sentiment_display}</p>", unsafe_allow_html=True)
                    else:
                        col2.markdown(f"<p style='color:{category_color}; font-size:18px;'>{sentiment_display}</p>", unsafe_allow_html=True)
            else:
                st.write(f"Hotel '{hotel_name_input}' not found in the summary data.")

        # Top 5 Hotels by Selected Category
        st.subheader("Top 5 Hotels by Selected Sentiment Category")
        category_options = {
            'Overall': 'avg_sentiment', 'Food Quality': 'food_score', 
            'Service Quality': 'service_score', 'Staff Friendliness': 'staff_score',
            'Cleanliness': 'cleanliness_score', 'Ambiance': 'ambiance_score',
            'Value for Money': 'value_score', 'Room Comfort': 'room_score',
            'Amenities': 'amenities_score'
        }
        selected_category = st.selectbox("Choose Sentiment Category", list(category_options.keys()))
        category_column = category_options[selected_category]
        top_hotels = hotel_sentiment_df.nlargest(5, category_column)
        st.table(top_hotels[['hotel_name', category_column]].rename(columns={category_column: f"{selected_category} Score"}))

        # Plot line chart for top 5 hotels
        st.subheader(f"Top 5 Hotels for {selected_category}")
        plt.figure(figsize=(8, 5))

        # Sorting hotels by score for a natural progression in the line plot
        top_hotels = top_hotels.sort_values(by=category_column, ascending=True)

        # Line plot
        plt.plot(top_hotels[category_column], top_hotels['hotel_name'], marker='o', linestyle='-', color="b")
        plt.xlabel(f"{selected_category} Score")
        plt.ylabel("Hotel Name")
        plt.grid(axis='x', linestyle='--', alpha=0.7)

        st.pyplot(plt)
    else:
        st.warning("Please upload all required files to proceed.")
