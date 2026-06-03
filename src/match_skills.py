"""
Module 3: Skill Matching and Scoring (NLTK-free version)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_skills(skills_file):
    """
    Load skills from text file
    
    Parameters:
        skills_file: Path to the skills.txt file
    
    Returns:
        List of skills (all lowercase, stripped of whitespace)
    """
    try:
        with open(skills_file, 'r', encoding='utf-8') as file:
            skills = []
            for line in file.readlines():
                skill = line.strip().lower()
                if skill:  # Only add non-empty lines
                    skills.append(skill)
        
        print(f"  ✓ Loaded {len(skills)} skills from skills file")
        return skills
    
    except FileNotFoundError:
        print(f"  ❌ Skills file not found: {skills_file}")
        return []
    
    except Exception as e:
        print(f"  ❌ Error loading skills: {e}")
        return []


def match_skills(resume_tokens, skill_list):
    """
    Match skills with resume tokens and calculate match score
    
    Parameters:
        resume_tokens: List of preprocessed tokens from resume
        skill_list: List of target skills to match against
    
    Returns:
        score: Float (0-100) representing match percentage
        matched_skills: List of skills that were found in the resume
    """
    if not resume_tokens:
        return 0, []
    
    if not skill_list:
        return 0, []
    
    matched_skills = []
    
    # Convert resume tokens to set for faster lookup
    resume_tokens_set = set(resume_tokens)
    
    # Check each skill
    for skill in skill_list:
        # Split multi-word skills (e.g., "machine learning" -> ["machine", "learning"])
        skill_parts = skill.split()
        
        if len(skill_parts) == 1:
            # Single word skill - direct match
            if skill in resume_tokens_set:
                matched_skills.append(skill)
        else:
            # Multi-word skill - check if all parts are in resume tokens
            # This is a simplified check - for better accuracy, we'd check sequence
            all_parts_found = all(part in resume_tokens_set for part in skill_parts)
            if all_parts_found:
                matched_skills.append(skill)
    
    # Calculate percentage score
    score = (len(matched_skills) / len(skill_list)) * 100
    
    return score, matched_skills


def get_missing_skills(matched_skills, all_skills):
    """
    Return list of skills that were not matched
    
    Parameters:
        matched_skills: List of skills that were found
        all_skills: List of all required skills
    
    Returns:
        List of skills that are missing from the resume
    """
    return [skill for skill in all_skills if skill not in matched_skills]


def calculate_score_details(resume_tokens, skill_list):
    """
    Calculate detailed match information
    
    Returns:
        Dictionary with score, matched, missing, and percentage
    """
    score, matched = match_skills(resume_tokens, skill_list)
    missing = get_missing_skills(matched, skill_list)
    
    return {
        'score': score,
        'matched_count': len(matched),
        'total_skills': len(skill_list),
        'percentage': f"{score:.2f}%",
        'matched_skills': matched,
        'missing_skills': missing
    }


# Test the module
if __name__ == "__main__":
    print("Testing Skill Matching Module")
    print("-" * 40)
    
    # Sample skills
    sample_skills = ['python', 'machine learning', 'sql', 'nlp']
    
    # Sample tokens
    sample_tokens = ['python', 'develop', 'machin', 'learn', 'sql', 'nlp']
    
    print(f"Skills to match: {sample_skills}")
    print(f"Resume tokens: {sample_tokens}")
    
    score, matched = match_skills(sample_tokens, sample_skills)
    missing = get_missing_skills(matched, sample_skills)
    
    print(f"\nResults:")
    print(f"  Score: {score:.2f}%")
    print(f"  Matched: {matched}")
    print(f"  Missing: {missing}")