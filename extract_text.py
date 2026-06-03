"""
Module 1: Text Extraction from Resume Files
Supports PDF and DOCX formats
"""

import PyPDF2
from docx import Document
import os
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def extract_from_pdf(file_path):
    """
    Extract text from a PDF file
    
    Parameters:
        file_path: Path to the PDF file
    
    Returns:
        Extracted text as string
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            
            # Extract text from each page
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            return text.strip()
    
    except Exception as e:
        print(f"  ⚠️ Error reading PDF {os.path.basename(file_path)}: {e}")
        return ""


def extract_from_docx(file_path):
    """
    Extract text from a DOCX file
    
    Parameters:
        file_path: Path to the DOCX file
    
    Returns:
        Extracted text as string
    """
    try:
        doc = Document(file_path)
        text = ""
        
        # Extract text from each paragraph
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"
        
        return text.strip()
    
    except Exception as e:
        print(f"  ⚠️ Error reading DOCX {os.path.basename(file_path)}: {e}")
        return ""


def extract_text(file_path):
    """
    Extract text from any supported file format
    
    Parameters:
        file_path: Path to the resume file
    
    Returns:
        Extracted text as string
    """
    if not os.path.exists(file_path):
        print(f"  ❌ File not found: {file_path}")
        return ""
    
    if file_path.endswith('.pdf'):
        return extract_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_from_docx(file_path)
    else:
        print(f"  ⚠️ Unsupported format: {file_path}")
        return ""


# Test the module when run directly
if __name__ == "__main__":
    print("Testing Text Extraction Module")
    print("-" * 40)
    
    # Find first resume file to test
    import glob
    test_files = glob.glob(os.path.join(config.RESUME_DIR, '*.*'))
    
    if test_files:
        test_file = test_files[0]
        print(f"Testing on: {os.path.basename(test_file)}")
        extracted_text = extract_text(test_file)
        
        print(f"✓ Extracted {len(extracted_text)} characters")
        print("\nFirst 500 characters:")
        print("-" * 40)
        print(extracted_text[:500])
        print("-" * 40)
    else:
        print(f"⚠️ No resume files found in: {config.RESUME_DIR}")
        print("Please add resume files (.pdf or .docx) to the resumes folder")