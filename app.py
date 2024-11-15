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
    hotel_sentiment_file = st.sidebar.file_uploader("Upload summary_review_1 file", type="csv", key="sentiment")
    review_details_file = st.sidebar.file_uploader("Upload indi_reviews file", type="csv", key="review_details")
    all_reviews_file = st.sidebar.file_uploader("Upload all_Reviews file", type="csv", key="all_reviews")

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
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(hotel_counts.values, labels=hotel_counts.index, autopct=None, startangle=140, colors=sns.color_palette("cubehelix", len(hotel_counts)))
        ax.set_title(f"Top Hotels in {selected_country}")
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
    #----------------------------------new-------------------------------
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
        st.subheader("Preferred Countries for Hotels")
        country_choices = pd.concat([data['Country1'], data['Country2']])
        country_counts = country_choices.value_counts()
    
        country_pie_fig, country_pie_ax = plt.subplots(figsize=(8, 10))
        country_pie_ax.pie(country_counts, labels=country_counts.index, startangle=90, 
                           colors=sns.color_palette("Set3", len(country_counts)))
        country_pie_ax.set_title("Preferred Countries for Hotels")
        country_pie_ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
        st.pyplot(country_pie_fig)
    
        # Hospitality Department Choices by Culinary Department
        st.subheader("Hospitality Department Choices by Culinary Department")
        dept_combinations = data.groupby(['CAdept', 'Hdept']).size().unstack().fillna(0)
    
        dept_heatmap_fig, dept_heatmap_ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(dept_combinations, annot=True, cmap="Blues", fmt="g", ax=dept_heatmap_ax)
        dept_heatmap_ax.set_title("Hospitality Department Choices by Culinary Department")
        dept_heatmap_ax.set_xlabel("Hospitality Department")
        dept_heatmap_ax.set_ylabel("Culinary Department")
        st.pyplot(dept_heatmap_fig)
    
        # Top Countries Where Students Prefer to Stay
        stay_choice = "Yes"
        stay_data = data[data['stay'] == stay_choice]
        country_choices_stay = pd.concat([stay_data['Country1'], stay_data['Country2']])
        country_counts_stay = country_choices_stay.value_counts()
    
        stay_pie_fig, stay_pie_ax = plt.subplots(figsize=(6, 6))
        stay_pie_ax.pie(country_counts_stay, labels=country_counts_stay.index, autopct='%1.1f%%',
                         startangle=90, colors=sns.color_palette("Set3", len(country_counts_stay)))
        stay_pie_ax.set_title("Top Countries Where Students Prefer to Stay")
        stay_pie_ax.axis('equal')
        st.pyplot(stay_pie_fig)
    
        # Preferred Countries for Hotels in CAdept
        st.subheader("Preferred Countries for working in specific Departments of CA and Hospitality")
        
        # Dropdown menu to select department
        departments = data['CAdept'].unique()  # Get unique departments from the data
        selected_dept = st.selectbox("Select Department", departments)
        
        # Filter data based on selected department
        dept_data = data[data['CAdept'] == selected_dept]
        country_choices_dept = pd.concat([dept_data['Country1'], dept_data['Country2']])
        country_counts_dept = country_choices_dept.value_counts()
    
        # Create a pie chart for the selected department
        dept_pie_fig, dept_pie_ax = plt.subplots(figsize=(5, 5))
        dept_pie_ax.pie(country_counts_dept, labels=country_counts_dept.index, autopct='%1.1f%%',
                         startangle=90, colors=sns.color_palette("rainbow", len(country_counts_dept)),
                         textprops={'fontsize': 5})
        dept_pie_ax.set_title(f"Preferred Countries for working in {selected_dept} Department")
        dept_pie_ax.axis('equal')
        st.pyplot(dept_pie_fig)
    
        # Filter data for the selected Hospitality Department
        selected_hdept = st.selectbox("Select Hospitality Department:", data['Hdept'].unique())
        hdept_data = data[data['Hdept'] == selected_hdept]
        
        # Combine Country1 and Country2 for the selected department
        country_choices_hdept = pd.concat([hdept_data['Country1'], hdept_data['Country2']])
        country_counts_hdept = country_choices_hdept.value_counts()
        
        # Create a pie chart for the selected Hospitality Department
        hdept_pie_fig, hdept_pie_ax = plt.subplots(figsize=(5, 5))
        hdept_pie_ax.pie(country_counts_hdept, labels=country_counts_hdept.index, autopct='%1.1f%%',
                          startangle=90, colors=sns.color_palette("Set3", len(country_counts_hdept)),
                          textprops={'fontsize': 6})  # Adjust font size for labels
        hdept_pie_ax.set_title(f"Preferred Countries for working in {selected_hdept} Department", fontsize=14)  # Title font size
        hdept_pie_ax.axis('equal')
        st.pyplot(hdept_pie_fig)
    
        # Future Career Aspirations by Country
        st.subheader("Future Career Aspirations by Country")
        g = sns.FacetGrid(data, col='future_career', col_wrap=3, height=5, sharey=False)
        g.map(sns.countplot, 'Country1', palette='Set2')
        g.set_axis_labels('Country', 'Number of Students')
        g.set_titles("{col_name}")
        g.set_xticklabels(rotation=45)
        plt.subplots_adjust(top=0.9, hspace=0.2)
        g.fig.suptitle('Future Career Aspirations by Country', fontsize=12)
        st.pyplot(g.fig)
    
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
