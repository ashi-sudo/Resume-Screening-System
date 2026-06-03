"""
Quick test script to verify all modules are working correctly
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """Test if all required libraries can be imported"""
    print("\n📦 Testing Library Imports...")
    print("-" * 40)
    
    libraries = [
        ('PyPDF2', 'PyPDF2'),
        ('python-docx', 'docx'),
        ('nltk', 'nltk'),
        ('pandas', 'pandas')
    ]
    
    all_ok = True
    for name, module in libraries:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError as e:
            print(f"  ❌ {name}: {e}")
            all_ok = False
    
    return all_ok


def test_custom_modules():
    """Test if custom modules can be imported"""
    print("\n📦 Testing Custom Modules...")
    print("-" * 40)
    
    modules = [
        'config',
        'src.extract_text',
        'src.preprocess',
        'src.match_skills',
        'src.rank_candidates'
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except Exception as e:
            print(f"  ❌ {module}: {e}")
            all_ok = False
    
    return all_ok


def test_config():
    """Test if configuration loads correctly"""
    print("\n📁 Testing Configuration...")
    print("-" * 40)
    
    try:
        import config
        print(f"  ✅ Config loaded")
        print(f"     Resumes folder: {config.RESUME_DIR}")
        print(f"     Output folder: {config.OUTPUT_DIR}")
        print(f"     Data folder: {config.DATA_DIR}")
        print(f"     Skills file: {config.SKILLS_FILE}")
        
        # Check if folders exist
        print(f"\n  📂 Folder Status:")
        print(f"     Resumes folder exists: {os.path.exists(config.RESUME_DIR)}")
        print(f"     Output folder exists: {os.path.exists(config.OUTPUT_DIR)}")
        print(f"     Data folder exists: {os.path.exists(config.DATA_DIR)}")
        
        return True
    except Exception as e:
        print(f"  ❌ Config error: {e}")
        return False


def test_skills_file():
    """Test if skills file exists and has content"""
    print("\n📋 Testing Skills File...")
    print("-" * 40)
    
    try:
        import config
        if os.path.exists(config.SKILLS_FILE):
            with open(config.SKILLS_FILE, 'r') as f:
                skills = [line.strip() for line in f.readlines() if line.strip()]
            print(f"  ✅ Skills file found")
            print(f"     Number of skills: {len(skills)}")
            print(f"     First 5 skills: {skills[:5]}")
            return True
        else:
            print(f"  ❌ Skills file not found: {config.SKILLS_FILE}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_resumes():
    """Test if resumes exist in the resumes folder"""
    print("\n📄 Testing Resumes...")
    print("-" * 40)
    
    try:
        import config
        import glob
        
        resumes = glob.glob(os.path.join(config.RESUME_DIR, '*.*'))
        
        if resumes:
            print(f"  ✅ Found {len(resumes)} resume(s)")
            for resume in resumes[:5]:  # Show first 5
                print(f"     - {os.path.basename(resume)}")
            return True
        else:
            print(f"  ⚠️ No resumes found in: {config.RESUME_DIR}")
            print(f"     Run: python tests/create_sample_resumes.py")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def run_all_tests():
    """Run all tests and show summary"""
    print("\n" + "="*60)
    print("🔍 SYSTEM TEST - Resume Screening Project")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Library Imports", test_imports()))
    results.append(("Custom Modules", test_custom_modules()))
    results.append(("Configuration", test_config()))
    results.append(("Skills File", test_skills_file()))
    results.append(("Resumes", test_resumes()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, status in results if status)
    total = len(results)
    
    for name, status in results:
        symbol = "✅" if status else "❌"
        print(f"  {symbol} {name}")
    
    print("-" * 40)
    print(f"  Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your system is ready to run.")
        print("   Run: python main.py")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
    
    print("="*60)


if __name__ == "__main__":
    run_all_tests()