import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.cache.clear()

# Sidebar for page selection
page = st.sidebar.selectbox("Choose a Page", ["SSCA Data Analysis", "Hotel Sentiment Analysis"])

# Loading the data
@st.cache
# Loading the data with file upload functionality
def load_ssca_data(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    else:
        st.error("Please upload the SSCA data CSV file.")
        return pd.DataFrame()

def load_hotel_data(uploaded_file1, uploaded_file2, uploaded_file3):
    if uploaded_file1 is not None and uploaded_file2 is not None and uploaded_file3 is not None:
        all_reviews_df = pd.read_csv(uploaded_file1)
        hotel_sentiment_df = pd.read_csv(uploaded_file2)
        review_details_df = pd.read_csv(uploaded_file3)
        return hotel_sentiment_df, review_details_df, all_reviews_df
    else:
        st.error("Please upload the required hotel data CSV files.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# ----------------SSCA Data Analysis Page----------------------------
if page == "SSCA Data Analysis":
    st.title("SSCA Data Analysis Dashboard")
    st.write("An interactive dashboard providing insights and visualizations on SSCA data.")
    # File uploader for SSCA data
    uploaded_ssca_file = st.file_uploader("Upload SSCA Data CSV", type=["csv"])
    
    if uploaded_ssca_file is not None:
        data = load_ssca_data(uploaded_ssca_file)
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

    # Age vs. Department Analysis
    st.subheader("Age Distribution by Culinary Department")
    fig, ax = plt.subplots()
    sns.boxplot(data=filtered_data, x="CAdept", y="Age", ax=ax, palette="Set3")
    ax.set_title("Age Distribution by Culinary Department")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Career Aspirations by Department
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
    selected_gender = st.radio("Select Gender:", data['Gender'].unique(), index=0)
    filtered_data_gender = data[data['Gender'] == selected_gender]
    countries_combined = pd.concat([filtered_data_gender['Country1'], filtered_data_gender['Country2']])
    country_counts = countries_combined.value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=country_counts.values, y=country_counts.index, palette="coolwarm", ax=ax)
    ax.set_title(f"Top Preferred Countries by {selected_gender}")
    ax.set_xlabel("Count")
    ax.set_ylabel("Country") 
    st.pyplot(fig)

    # Stay Intentions Analysis
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
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(hotel_counts.values, labels=hotel_counts.index, autopct=None, startangle=140, colors=sns.color_palette("cubehelix", len(hotel_counts)))
    ax.set_title(f"Top Hotels in {selected_country}")
    st.pyplot(fig)

    # Hotel Chains Analysis
    st.subheader("Hotel Chains Analysis")
    hotel_columns = ['C1hotel1', 'C1hotel2', 'C2hotel1', 'C2hotel2']
    hotel_names = pd.concat([data[col] for col in hotel_columns], ignore_index=True)
    hotel_names_cleaned = hotel_names.dropna().unique()

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

    # Stay Decisions by Hospitality Department
    st.subheader('Stay Decisions by Hospitality Department')
    stay_dept_fig, stay_dept_ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=data, x='Hdept', hue='stay', palette='muted', ax=stay_dept_ax)
    stay_dept_ax.set_title('Stay Decisions by Hospitality Department')
    stay_dept_ax.set_xlabel('Hospitality Department')
    stay_dept_ax.set_ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(stay_dept_fig)

    # Preferred Countries for Hotels
    st.subheader('Preferred Countries for Hotels')
    preferred_countries = pd.concat([data['Country1'], data['Country2']])
    country_preference_counts = preferred_countries.value_counts()
    country_pref_fig, country_pref_ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=country_preference_counts.index, y=country_preference_counts.values, palette="coolwarm", ax=country_pref_ax)
    country_pref_ax.set_title('Preferred Countries for Hotels')
    country_pref_ax.set_xlabel('Country')
    country_pref_ax.set_ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(country_pref_fig)

# ----------------Hotel Sentiment Analysis Page-------------------------
elif page == "Hotel Sentiment Analysis":
    st.title("Hotel Sentiment Analysis Dashboard")
    st.write("An interactive dashboard providing insights on hotel reviews, sentiment scores, and preferences.")
    uploaded_file1 = st.file_uploader("Upload All Reviews Data", type=["csv"])
    uploaded_file2 = st.file_uploader("Upload Hotel Sentiment Data", type=["csv"])
    uploaded_file3 = st.file_uploader("Upload Review Details Data", type=["csv"])
    
    if uploaded_file1 and uploaded_file2 and uploaded_file3:
        hotel_sentiment_df, review_details_df, all_reviews_df = load_hotel_data(uploaded_file1, uploaded_file2, uploaded_file3)
        
        st.write(hotel_sentiment_df)
        st.write(review_details_df)
        st.write(all_reviews_df)
        
        st.subheader('Top 10 Hotels by Sentiment Score')
        sentiment_scores = hotel_sentiment_df[['Hotel', 'Sentiment Score']].sort_values(by='Sentiment Score', ascending=False).head(10)
        st.write(sentiment_scores)
