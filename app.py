import streamlit as st
import pandas as pd
from textblob import TextBlob
import spacy
from nltk.corpus import wordnet
import nltk

# Download NLTK WordNet data
nltk.download('wordnet')

# Load spaCy's English language model
nlp = spacy.load("en_core_web_sm")

# Define initial category patterns (you can add or modify these)
categories = {
    "Food Quality": ["food", "delicious", "taste", "cuisine", "meal", "dish"],
    "Service Quality": ["service", "assistance", "helpful", "support"],
    "Staff Friendliness": ["polite", "friendly", "knowledgeable", "helpful"],
    "Cleanliness": ["clean", "hygiene", "sanitary", "spotless"],
    "Ambiance": ["welcoming", "cozy", "elegant", "charming", "vibrant"],
    "Value for Money": ["value", "affordable", "pricing", "overpriced"],
    "Room Comfort": ["luxurious", "comfortable", "spacious", "view", "amenities"],
    "Amenities": ["facility", "pool", "spa", "gym"]
}

# Define helper functions
def expand_category_terms(terms):
    expanded_terms = set(terms)
    for term in terms:
        synonyms = wordnet.synsets(term)
        for syn in synonyms:
            for lemma in syn.lemmas():
                expanded_terms.add(lemma.name().replace('_', ' '))
    return list(expanded_terms)

# Expand terms for each category
for category, terms in categories.items():
    categories[category] = expand_category_terms(terms)

def categorize_and_score(text, category):
    doc = nlp(text.lower())
    relevant_sentences = []
    for sentence in doc.sents:
        if any(term in sentence.text for term in categories[category]):
            relevant_sentences.append(sentence.text)
    if relevant_sentences:
        scores = [TextBlob(sentence).sentiment.polarity for sentence in relevant_sentences]
        return sum(scores) / len(scores)
    return None

# Main app
st.title("Hotel Review Sentiment Analysis")
st.write("Upload your CSV file containing hotel reviews to analyze.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file:
    # Load data
    reviews_df = pd.read_csv(uploaded_file)
    
    # Process reviews and calculate category scores
    reviews_df['Sentiment Score'] = reviews_df['Review Text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    reviews_df['Sentiment'] = reviews_df['Sentiment Score'].apply(lambda x: 'positive' if x > 0.1 else ('negative' if x < -0.1 else 'neutral'))
    
    for category in categories.keys():
        reviews_df[f'{category} Score'] = reviews_df['Review Text'].apply(lambda x: categorize_and_score(str(x), category))
    
    st.write("Processed Reviews:")
    st.dataframe(reviews_df)

    # Save to CSV
    st.write("Download processed review data:")
    st.download_button(
        label="Download CSV",
        data=reviews_df.to_csv(index=False).encode('utf-8'),
        file_name='processed_reviews.csv',
        mime='text/csv'
    )
