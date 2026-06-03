"""
Module 4: Candidate Ranking System (NLTK-free version)
Processes all resumes and ranks them by match score
"""

import os
import pandas as pd
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.extract_text import extract_text
from src.simple_preprocess import preprocess_text  # Changed to simple_preprocess
from src.match_skills import load_skills, match_skills, get_missing_skills


def get_all_resumes():
    """
    Get all resume files from the resumes folder
    
    Returns:
        List of dictionaries with 'name' and 'path' keys
    """
    resumes = []
    
    if not os.path.exists(config.RESUME_DIR):
        print(f"❌ Resumes folder not found: {config.RESUME_DIR}")
        return resumes
    
    for file in os.listdir(config.RESUME_DIR):
        if file.lower().endswith(config.SUPPORTED_FORMATS):
            file_path = os.path.join(config.RESUME_DIR, file)
            resumes.append({
                'name': file,
                'path': file_path
            })
    
    return resumes


def process_single_resume(resume_info, skills):
    """
    Process one resume and return match results
    """
    filename = resume_info['name']
    filepath = resume_info['path']
    
    # Step 1: Extract text
    raw_text = extract_text(filepath)
    
    if not raw_text:
        return {
            'Resume': filename,
            'Score (%)': 0,
            'Matched Skills': 'Extraction failed',
            'Skills Count': 0,
            'Missing Skills': 'N/A'
        }
    
    # Step 2: Preprocess (using simple_preprocess)
    cleaned_tokens = preprocess_text(raw_text, verbose=False)
    
    if not cleaned_tokens:
        return {
            'Resume': filename,
            'Score (%)': 0,
            'Matched Skills': 'No text extracted',
            'Skills Count': 0,
            'Missing Skills': 'All skills missing'
        }
    
    # Step 3: Match skills
    score, matched = match_skills(cleaned_tokens, skills)
    missing = get_missing_skills(matched, skills)
    
    return {
        'Resume': filename,
        'Score (%)': round(score, 2),
        'Matched Skills': ', '.join(matched) if matched else 'None',
        'Skills Count': len(matched),
        'Missing Skills': ', '.join(missing[:5]) if missing else 'None'
    }


def rank_all_candidates():
    """
    Main function to process all resumes and return ranked results
    """
    print("\n" + "="*60)
    print("🎯 RESUME SCREENING SYSTEM")
    print("="*60)
    
    # Check if skills file exists
    if not os.path.exists(config.SKILLS_FILE):
        print(f"\n❌ Skills file not found: {config.SKILLS_FILE}")
        print("   Please create data/skills.txt with one skill per line")
        return None
    
    # Load skills
    print(f"\n📋 Loading skills...")
    skills = load_skills(config.SKILLS_FILE)
    
    if not skills:
        print("   ❌ No skills found in file")
        return None
    
    # Get all resumes
    print(f"\n📁 Scanning for resumes...")
    resumes = get_all_resumes()
    print(f"   ✓ Found {len(resumes)} resume(s)")
    
    if len(resumes) == 0:
        print("\n⚠️ No resumes found! Please add .pdf or .docx files to the 'resumes' folder")
        return None
    
    # Process each resume
    print("\n🔄 Processing resumes...")
    print("-" * 50)
    
    results = []
    for idx, resume in enumerate(resumes, 1):
        print(f"\n{idx}. Processing: {resume['name']}")
        result = process_single_resume(resume, skills)
        print(f"   ✅ Score: {result['Score (%)']}% (Matched: {result['Skills Count']}/{len(skills)})")
        results.append(result)
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Sort by score (highest first)
    df = df.sort_values('Score (%)', ascending=False).reset_index(drop=True)
    df.insert(0, 'Rank', range(1, len(df) + 1))
    
    return df


def display_results(df):
    """Display results in a nicely formatted table"""
    if df is None or df.empty:
        print("\n❌ No results to display")
        return
    
    print("\n" + "="*70)
    print("🏆 RANKED CANDIDATES")
    print("="*70)
    
    for _, row in df.iterrows():
        print(f"\n🥇 Rank #{row['Rank']}: {row['Resume']}")
        print(f"   📊 Match Score: {row['Score (%)']}%")
        print(f"   🎯 Skills Found: {row['Skills Count']}")
        
        # Progress bar
        bar_length = int(row['Score (%)'] / 2)
        bar = '█' * bar_length + '░' * (50 - bar_length)
        print(f"   {bar} {row['Score (%)']}%")
        
        # Show matched skills
        if row['Matched Skills'] != 'None' and row['Matched Skills'] != 'Extraction failed':
            matched_list = row['Matched Skills'].split(', ')
            if len(matched_list) > 5:
                print(f"   ✅ Matched: {', '.join(matched_list[:5])}...")
            else:
                print(f"   ✅ Matched: {row['Matched Skills']}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY REPORT")
    print("="*70)
    print(f"   📄 Total Resumes: {len(df)}")
    print(f"   📈 Average Score: {df['Score (%)'].mean():.2f}%")
    print(f"   🏆 Highest Score: {df['Score (%)'].max():.2f}%")
    
    if len(df) > 0:
        top = df.iloc[0]
        print(f"\n   🎉 TOP CANDIDATE: {top['Resume']}")
        print(f"      Score: {top['Score (%)']}%")
    
    print("\n" + "="*70)


def save_results(df):
    """Save results to CSV files"""
    if df is None or df.empty:
        return
    
    full_path = config.RESULTS_CSV
    df.to_csv(full_path, index=False)
    print(f"\n💾 Results saved to: {full_path}")
    
    simple_df = df[['Rank', 'Resume', 'Score (%)', 'Skills Count']]
    simple_path = config.SIMPLE_RESULTS_CSV
    simple_df.to_csv(simple_path, index=False)
    print(f"💾 Simple results saved to: {simple_path}")


if __name__ == "__main__":
    results_df = rank_all_candidates()
    if results_df is not None:
        display_results(results_df)
        save_results(results_df)
