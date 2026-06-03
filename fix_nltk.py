"""
Fix NLTK data issues
Run this script to properly download NLTK data
"""

import nltk
import os
import sys

def fix_nltk():
    print("="*50)
    print("🔧 FIXING NLTK DATA")
    print("="*50)
    
    # Set a custom path for NLTK data
    nltk_data_path = os.path.join(os.path.expanduser("~"), "nltk_data_custom")
    
    # Add to NLTK search path
    if nltk_data_path not in nltk.data.path:
        nltk.data.path.insert(0, nltk_data_path)
    
    # Create directory if it doesn't exist
    os.makedirs(nltk_data_path, exist_ok=True)
    
    print(f"\n📁 Using NLTK data path: {nltk_data_path}")
    
    # Download required data
    print("\n📥 Downloading required NLTK data...")
    
    try:
        # Download stopwords
        print("  - Downloading stopwords...")
        nltk.download('stopwords', download_dir=nltk_data_path, quiet=False)
        
        # Download punkt tokenizer
        print("  - Downloading punkt tokenizer...")
        nltk.download('punkt', download_dir=nltk_data_path, quiet=False)
        
        # Download averaged_perceptron_tagger (optional but good)
        print("  - Downloading tagger...")
        nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_path, quiet=False)
        
        print("\n✅ All NLTK data downloaded successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading NLTK data: {e}")
        return False

def test_nltk():
    """Test if NLTK is working"""
    print("\n" + "="*50)
    print("🧪 TESTING NLTK")
    print("="*50)
    
    try:
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        
        # Test stopwords
        stops = stopwords.words('english')
        print(f"\n✅ Stopwords loaded: {len(stops)} words")
        print(f"   Example: {stops[:10]}")
        
        # Test tokenization
        test_text = "This is a test sentence."
        tokens = word_tokenize(test_text)
        print(f"\n✅ Tokenization working: {tokens}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    if fix_nltk():
        print("\n" + "="*50)
        test_nltk()
        print("\n" + "="*50)
        print("✅ NLTK fix complete!")
        print("Now run: python main.py")
    else:
        print("\n❌ Failed to fix NLTK")
        print("Please try: python -m pip install --upgrade nltk")