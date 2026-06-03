"""
Module 2: Text Preprocessing for NLP
Includes: Lowercase, punctuation removal, tokenization, stopwords removal, stemming
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def download_nltk_data():
    """Download required NLTK data if not already present"""
    try:
        nltk.data.find('tokenizers/punkt')
        print("✓ NLTK data already downloaded")
    except LookupError:
        print("📥 Downloading NLTK data (first time only)...")
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        print("✓ NLTK data downloaded successfully")


# Download NLTK data when module loads
download_nltk_data()

# Initialize NLP tools
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


def preprocess_text(text, verbose=False):
    """
    Clean and preprocess text for NLP tasks
    
    Steps performed:
    1. Convert to lowercase
    2. Remove punctuation and numbers
    3. Tokenize (split into words)
    4. Remove stopwords (common words like 'the', 'and', etc.)
    5. Stem words (reduce to root form)
    
    Parameters:
        text: String to preprocess
        verbose: If True, prints step-by-step output for debugging
    
    Returns:
        List of preprocessed tokens (words)
    """
    if not text:
        return []
    
    if verbose:
        print("\n  📝 Preprocessing steps:")
    
    # Step 1: Convert to lowercase
    text = text.lower()
    if verbose:
        print(f"    1. Lowercase: {text[:80]}...")
    
    # Step 2: Remove punctuation and numbers (keep only letters and spaces)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    if verbose:
        print(f"    2. Cleaned: {text[:80]}...")
    
    # Step 3: Split into words (tokenization)
    tokens = text.split()
    if verbose:
        print(f"    3. Tokens: {tokens[:10]}...")
    
    # Step 4: Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    if verbose:
        print(f"    4. Without stopwords: {tokens[:10]}...")
    
    # Step 5: Stemming (reduce words to root form)
    tokens = [stemmer.stem(word) for word in tokens]
    if verbose:
        print(f"    5. Stemmed: {tokens[:10]}...")
        print(f"  ✓ Preprocessing complete. {len(tokens)} tokens remaining")
    
    return tokens


def get_stopwords_list():
    """Return list of English stopwords for reference"""
    return list(stop_words)


# Test the module when run directly
if __name__ == "__main__":
    print("Testing Preprocessing Module")
    print("-" * 40)
    
    sample_text = """
    I am a Python developer with 5 years of experience in Machine Learning 
    and Natural Language Processing. I have worked on many exciting projects 
    using TensorFlow and PyTorch.
    """
    
    print("Original text:")
    print(f'"{sample_text.strip()}"')
    print("\n" + "-" * 40)
    
    # Test with verbose mode
    result = preprocess_text(sample_text, verbose=True)
    
    print("\n" + "-" * 40)
    print(f"Final tokens: {result}")
    print(f"Total tokens: {len(result)}")