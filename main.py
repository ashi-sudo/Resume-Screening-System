"""
Resume Screening System - Main Entry Point
AI Lab Project - NLP Based Candidate Ranking
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules
from src.rank_candidates import rank_all_candidates, display_results, save_results


def main():
    """Main function to run the resume screening system"""
    
    print("\n" + "="*70)
    print("🌟 WELCOME TO RESUME SCREENING SYSTEM")
    print("   AI Lab Project - NLP Based Candidate Ranking")
    print("="*70)
    
    print("\n📌 System Features:")
    print("   ✓ Text extraction from PDF/DOCX files")
    print("   ✓ NLP preprocessing (tokenization, stopwords, stemming)")
    print("   ✓ Skill matching and scoring")
    print("   ✓ Candidate ranking")
    print("   ✓ Results export to CSV")
    
    # Run the screening
    results_df = rank_all_candidates()
    
    # Display and save results
    if results_df is not None and not results_df.empty:
        display_results(results_df)
        save_results(results_df)
        print("\n✨ Screening completed successfully!")
        print("   Check the 'output' folder for CSV results.")
    else:
        print("\n❌ Screening failed. Please check:")
        print("   1. 'resumes' folder contains PDF/DOCX files")
        print("   2. 'data/skills.txt' exists and has skills listed")
        print("   3. All required libraries are installed")
    
    print("\n👋 Thank you for using Resume Screening System!")


if __name__ == "__main__":
    main()