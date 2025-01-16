import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
import seaborn as sns
import matplotlib.pyplot as plt

# Download necessary NLTK data
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

# Load Dataset
def load_data():
    # Replace with your dataset path or scraping logic
    url = "https://raw.githubusercontent.com/dD2405/Twitter_Sentiment_Analysis/master/train.csv"
    data = pd.read_csv(url)
    return data

# Text Preprocessing
def preprocess_text(text):
    # Lowercase conversion
    text = text.lower()
    # Remove special characters, numbers, and punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenization
    tokens = word_tokenize(text)
    # Stopwords removal
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

# Main pipeline
def main():
    # Step 1: Load Data
    data = load_data()
    
    # Ensure the dataset has necessary columns
    if 'tweet' not in data.columns or 'label' not in data.columns:
        print("Dataset must contain 'tweet' and 'label' columns.")
        return

    # Map labels to sentiments (assuming 0=negative, 1=neutral, 2=positive)
    data['label'] = data['label'].map({0: 'Negative', 1: 'Neutral', 2: 'Positive'})

    # Step 2: Preprocess Text
    print("Preprocessing text data...")
    data['cleaned_text'] = data['tweet'].apply(preprocess_text)

    # Step 3: Vectorization using TF-IDF
    print("Vectorizing text data...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(data['cleaned_text']).toarray()
    y = data['label']

    # Step 4: Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 5: Model Training
    print("Training model...")
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Step 6: Model Evaluation
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred, labels=['Negative', 'Neutral', 'Positive'])
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=['Negative', 'Neutral', 'Positive'], 
                yticklabels=['Negative', 'Neutral', 'Positive'], cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.show()

if __name__ == "__main__":
    main()
