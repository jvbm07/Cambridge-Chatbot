import json
import streamlit as st
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import io

def load_data(file):
    """Load JSON data from a file-like object."""
    return json.load(file)['data']

def generate_word_cloud(text):
    """Generate a word cloud image."""
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud.to_image()

def most_used_words(text, n=10):
    """Return the most used words."""
    vectorizer = CountVectorizer(stop_words='english')
    word_count = vectorizer.fit_transform([text])
    sum_words = word_count.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]

def profile_data(data):
    """Provide basic profiling of the data."""
    ages = [item['age'] for item in data]
    experience = [item['years_of_experience'] for item in data]
    industries = [item['primary_industry'] for item in data]
    
    avg_age = sum(ages) / len(ages)
    avg_experience = sum(experience) / len(experience)
    common_industry = Counter(industries).most_common(1)[0][0]
    
    return avg_age, avg_experience, common_industry

def analyze_data(data):
    """Analyze the JSON data for insights."""
    # Combine all text fields for word analysis
    combined_text = ' '.join([
        item['role'] + ' ' + item['primary_industry'] + ' ' + item['current_challenges'] + ' ' + ' '.join(item['goals'])
        for item in data
    ])
    
    # Generate word cloud
    wordcloud_image = generate_word_cloud(combined_text)
    
    # Most used words
    top_words = most_used_words(combined_text)
    
    # Data profiling
    avg_age, avg_experience, common_industry = profile_data(data)
    
    return wordcloud_image, top_words, avg_age, avg_experience, common_industry

def main():
    st.title('Data Insights')
    
    # Upload file
    uploaded_file = st.file_uploader("Choose a JSON file", type="json")
    
    if uploaded_file is not None:
        # Read the JSON file
        data = load_data(uploaded_file)
        
        # Analyze data
        wordcloud_image, top_words, avg_age, avg_experience, common_industry = analyze_data(data)

        # Display results
        st.subheader("Word Cloud")
        st.image(wordcloud_image)
        
        st.subheader("Most Used Words")
        top_words_df = pd.DataFrame(top_words, columns=["Word", "Frequency"])
        st.write(top_words_df)
        
        st.subheader("Data Profiling")
        st.write(f"Average Age: {avg_age:.2f}")
        st.write(f"Average Years of Experience: {avg_experience:.2f}")
        st.write(f"Most Common Industry: {common_industry}")

if __name__ == "__main__":
    main()
