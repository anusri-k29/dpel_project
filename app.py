import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
st.cache_data.clear()
# Sidebar for page selection
page = st.sidebar.selectbox("Choose a Page", ["SSCA Data Analysis", "Hotel Sentiment Analysis"])

# Loading the data
@st.cache_data
def load_ssca_data():
    return pd.read_csv('SSCA_final_data.csv')

@st.cache_data
def load_hotel_data():
    try:
        all_reviews_df = pd.read_csv('all_reviews.csv')
        hotel_sentiment_df = pd.read_csv('summary_review_1.csv')
        review_details_df = pd.read_csv('indi_reviews.csv')
    except FileNotFoundError:
        st.error("One or more required files are missing.")
        return pd.DataFrame(), pd.DataFrame()
    return hotel_sentiment_df, review_details_df, all_reviews_df

# ----------------SSCA Data Analysis Page----------------------------
if page == "SSCA Data Analysis":
    data = load_ssca_data()
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

#  Age vs. Department Analysis
    st.subheader("Age Distribution by Culinary Department")
    filtered_data_dept = data  # No filtering by department
    fig, ax = plt.subplots()
    sns.boxplot(data=filtered_data_dept, x="CAdept", y="Age", ax=ax, palette="Set3")
    ax.set_title("Age Distribution by Culinary Department")
    plt.xticks(rotation=45)
    st.pyplot(fig)
#  Career Aspirations by Department
    st.subheader("Career Aspirations by Culinary Department")
    career_dept_counts = data.groupby(['CAdept', 'future_career']).size().unstack().fillna(0)
    fig, ax = plt.subplots()
    career_dept_counts.plot(kind='bar', stacked=True, ax=ax, colormap="viridis")
    ax.set_title("Career Aspirations by Culinary Department")
    ax.set_xlabel("Culinary Department")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    st.pyplot(fig)
# Gender and Country Preferences
    st.subheader("Gender and Country Preferences")
    # Select gender and filter data
    selected_gender = st.radio("Select Gender:", data['Gender'].unique(), index=0)
    filtered_data_gender = data[data['Gender'] == selected_gender]
    # Combine Country1 and Country2 columns 
    countries_combined = pd.concat([filtered_data_gender['Country1'], filtered_data_gender['Country2']])
    country_counts = countries_combined.value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=country_counts.values, y=country_counts.index, palette="coolwarm", ax=ax)
    ax.set_title(f"Top Preferred Countries by {selected_gender}")
    ax.set_xlabel("Count")
    ax.set_ylabel("Country") 
    st.pyplot(fig)
#  Stay Intentions Analysis
    st.subheader("Stay Intentions")
    stay_counts = data['stay'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(stay_counts, labels=stay_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    ax.set_title("Stay Intentions")
    st.pyplot(fig)
# Top Hotel Preferences per Country
    st.subheader("Top Hotel Preferences by Country")
    selected_country = st.selectbox("Select Country:", data['Country1'].unique())
    country_hotels = data[data['Country1'] == selected_country][['C1hotel1', 'C1hotel2']].melt(value_name='Hotels').dropna()
    hotel_counts = country_hotels['Hotels'].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=hotel_counts.values, y=hotel_counts.index, palette="cubehelix", ax=ax)
    ax.set_title(f"Top Hotels in {selected_country}")
    ax.set_xlabel("Count")
    st.pyplot(fig)

        # --- Extract and Map Hotel Chains ---
    st.subheader("Hotel Chains Analysis")
    
    # Define columns with hotel names
    hotel_columns = ['C1hotel1', 'C1hotel2', 'C2hotel1', 'C2hotel2']
    
    # Extract hotel names from columns, remove duplicates and NaNs
    hotel_names = pd.concat([data[col] for col in hotel_columns], ignore_index=True)
    hotel_names_cleaned = hotel_names.dropna().unique()
    
    # Function to map hotels to hotel chains
    def map_to_hotel_chain(hotel_name):
        hotel_name = str(hotel_name).lower()
        if 'taj' in hotel_name:
            return 'Taj Hotels'
        elif 'hilton' in hotel_name:
            return 'Hilton Hotels'
        elif 'st regis' in hotel_name:
            return 'St. Regis Hotels'
        elif 'jw marriott' in hotel_name:
            return 'JW Marriott'
        elif 'marriott' in hotel_name:
            return 'Marriott Hotels'
        elif 'ritz' in hotel_name or 'ritz-carlton' in hotel_name:
            return 'Ritz-Carlton'
        elif 'hyatt' in hotel_name:
            return 'Hyatt Hotels'
        elif 'sofitel' in hotel_name:
            return 'Sofitel Hotels'
        elif 'shangri-la' in hotel_name:
            return 'Shangri-La Hotels'
        elif 'oberoi' in hotel_name:
            return 'Oberoi Hotels'
        elif 'leela' in hotel_name:
            return 'Leela Palace'
        elif 'jumeirah' in hotel_name:
            return 'Jumeirah Hotels'
        elif 'itc' in hotel_name:
            return 'ITC Hotels'
        elif 'kempinski' in hotel_name:
            return 'Kempinski Hotels'
        elif 'bulgari' in hotel_name:
            return 'Bulgari Hotels'
        elif 'mandarin' in hotel_name:
            return 'Mandarin Oriental'
        elif 'rosewood' in hotel_name:
            return 'Rosewood Hotels'
        elif 'andaz' in hotel_name:
            return 'Andaz Hotels'
        else:
            return None
    hotel_chain_classes = [map_to_hotel_chain(name) for name in hotel_names_cleaned]
    df_hotel_chains = pd.DataFrame({'Hotel Name': hotel_names_cleaned, 'Hotel Chain': hotel_chain_classes})
    st.write("Hotel Chains Mapped from SSCA Data")
    hotel_chain_counts = df_hotel_chains['Hotel Chain'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=hotel_chain_counts.index, y=hotel_chain_counts.values, palette='viridis', ax=ax)
    ax.set_title("Distribution of Hotels by Chain")
    ax.set_xlabel("Hotel Chain")
    ax.set_ylabel("Number of Hotels")
    plt.xticks(rotation=45)
    st.pyplot(fig)
# ----------------------------Hotel Sentiment Analysis Page ----------------------------------------
if page == "Hotel Sentiment Analysis":
    hotel_sentiment_df, review_details_df, all_reviews_df = load_hotel_data()
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
    # Top Positive & Negative Reviews
    if hotel_name_input and not review_details_df.empty:
    hotel_name_input_cleaned = hotel_name_input.strip().lower()
    review_details_df['hotel_name_cleaned'] = review_details_df['hotel_name'].str.strip().str.lower()

    # Filter the reviews for the selected hotel
    hotel_reviews_for_selected_hotel = review_details_df[review_details_df['hotel_name_cleaned'].str.contains(hotel_name_input_cleaned)]
    
    if not hotel_reviews_for_selected_hotel.empty:
        # Sort by sentiment score for the selected hotel reviews
        hotel_reviews_sorted_by_sentiment = hotel_reviews_for_selected_hotel.sort_values(by='Sentiment Score', ascending=False)

        # Display top positive review
        st.subheader(f"Top Positive Review for {hotel_name_input}")
        top_positive_review = hotel_reviews_sorted_by_sentiment.iloc[0]
        st.write(f"**Rating:** {top_positive_review['Rating']}")
        st.write(f"**Review Title:** {top_positive_review['Review Title']}")
        st.write(f"**Review Text:** {top_positive_review['Review Text']}")
            
        # Display top negative review
        st.subheader(f"Top Negative Review for {hotel_name_input}")
        top_negative_review = hotel_reviews_sorted_by_sentiment.iloc[-1]
        st.write(f"**Rating:** {top_negative_review['Rating']}")
        st.write(f"**Review Title:** {top_negative_review['Review Title']}")
        st.write(f"**Review Text:** {top_negative_review['Review Text']}")
    else:
        st.write(f"No reviews available for {hotel_name_input}.")


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

    # Plot bar chart for top 5 hotels
    st.subheader(f"Top 5 Hotels for {selected_category}")
    plt.figure(figsize=(8, 5))
    sns.barplot(x=top_hotels[category_column], y=top_hotels['hotel_name'], palette="viridis")
    plt.xlabel(f"{selected_category} Score")
    plt.ylabel("Hotel Name")
    st.pyplot(plt)
      # --- Trip Type Analysis ---
    st.subheader("Trip Type Distribution")
    if 'Trip Type' in all_reviews_df.columns:
        
        trip_type_counts = all_reviews_df['Trip Type'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=trip_type_counts.index, y=trip_type_counts.values, palette="Set2", ax=ax)
        ax.set_title("Distribution of Trip Types")
        ax.set_xlabel("Trip Type")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.write("The 'Trip Type' column is missing from the dataset.")
