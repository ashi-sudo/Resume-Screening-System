"""
Simple Text Preprocessing without NLTK
No external dependencies needed
"""

import re

# Manual list of common English stopwords
STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'i', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were',
    'will', 'with', 'me', 'my', 'myself', 'we', 'our', 'ours', 'you', 'your', 'yours',
    'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves', 'am', 'are', 'was', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'but',
    'so', 'very', 'just', 'any', 'each', 'which', 'who', 'whom', 'this', 'that', 'these',
    'those', 'then', 'than', 'so', 'too', 'very', 'can', 'will', 'just', 'but', 'also',
    'if', 'then', 'else', 'when', 'where', 'which', 'while', 'would', 'could', 'should',
    'no', 'nor', 'not', 'only', 'own', 'same', 'such', 'up', 'down', 'off', 'over',
    'under', 'again', 'further', 'here', 'there', 'where', 'why', 'how'
}

def stem_word(word):
    """
    Simple stemming function - reduces words to root form
    """
    word = word.lower()
    
    # Remove common suffixes
    if len(word) > 5:
        if word.endswith('ing'):
            word = word[:-3]
        elif word.endswith('ed'):
            word = word[:-2]
        elif word.endswith('er'):
            word = word[:-2]
        elif word.endswith('ly'):
            word = word[:-2]
        elif word.endswith('s') and not word.endswith('ss'):
            word = word[:-1]
        elif word.endswith('ies'):
            word = word[:-3] + 'y'
        elif word.endswith('es'):
            word = word[:-2]
    
    return word

def preprocess_text(text, verbose=False):
    """
    Clean and preprocess text without NLTK
    
    Steps:
    1. Convert to lowercase
    2. Remove punctuation and numbers
    3. Split into words
    4. Remove stopwords
    5. Stem words
    
    Returns:
        List of processed tokens
    """
    if not text:
        return []
    
    if verbose:
        print("\n  📝 Preprocessing steps:")
    
    # Step 1: Lowercase
    text = text.lower()
    if verbose:
        print(f"    1. Lowercase: {text[:80]}...")
    
    # Step 2: Remove punctuation and numbers (keep only letters and spaces)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    if verbose:
        print(f"    2. Cleaned: {text[:80]}...")
    
    # Step 3: Split into words (tokenization)
    tokens = text.split()
    if verbose:
        print(f"    3. Tokens: {tokens[:10]}...")
    
    # Step 4: Remove stopwords and short words
    tokens = [word for word in tokens if word not in STOPWORDS and len(word) > 1]
    if verbose:
        print(f"    4. Without stopwords: {tokens[:10]}...")
    
    # Step 5: Stemming
    tokens = [stem_word(word) for word in tokens]
    if verbose:
        print(f"    5. Stemmed: {tokens[:10]}...")
        print(f"  ✓ Preprocessing complete. {len(tokens)} tokens remaining")
    
    return tokens

def simple_tokenize(text):
    """Simple tokenization function"""
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    return text.split()

# Test the module
if __name__ == "__main__":
    print("Testing Simple Preprocessing Module")
    print("-" * 40)
    
    sample = "I am a Python developer with machine learning and data science experience!"
    print(f"Original: {sample}")
    
    result = preprocess_text(sample, verbose=True)
    print(f"\nFinal: {result}")