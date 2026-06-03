"""
Configuration file for Resume Screening System
Centralized settings for the entire project
"""

import os

# Get the base directory (where this config file is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder paths
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESUME_DIR = os.path.join(BASE_DIR, 'resumes')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
SRC_DIR = os.path.join(BASE_DIR, 'src')
TESTS_DIR = os.path.join(BASE_DIR, 'tests')

# File paths
SKILLS_FILE = os.path.join(DATA_DIR, 'skills.txt')
RESULTS_CSV = os.path.join(OUTPUT_DIR, 'ranking_results.csv')
SIMPLE_RESULTS_CSV = os.path.join(OUTPUT_DIR, 'simple_results.csv')

# Supported file formats
SUPPORTED_FORMATS = ('.pdf', '.docx')

# Create necessary directories if they don't exist
os.makedirs(RESUME_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Display configuration when loaded
print("=" * 50)
print("📁 CONFIGURATION LOADED")
print("=" * 50)
print(f"Resumes folder: {RESUME_DIR}")
print(f"Output folder:  {OUTPUT_DIR}")
print(f"Data folder:    {DATA_DIR}")
print(f"Skills file:    {SKILLS_FILE}")
print("=" * 50)