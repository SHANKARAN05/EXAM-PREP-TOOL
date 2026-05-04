"""
Test script to verify the application setup
Run this after init_db.py to check if everything is working
"""

import os
import sys

def test_file_structure():
    """Test if all required files exist"""
    print("="*60)
    print("Testing File Structure...")
    print("="*60)
    
    required_files = [
        'app.py',
        'config.py',
        'init_db.py',
        'requirements.txt',
        'models/__init__.py',
        'models/database.py',
        'parser/__init__.py',
        'parser/java_parser.py',
        'parser/network_parser.py',
        'parser/os_parser.py',
        'routes/__init__.py',
        'routes/home.py',
        'routes/study.py',
        'routes/exam.py',
        'routes/results.py',
        'templates/base.html',
        'templates/home.html',
        'templates/study.html',
        'templates/exam.html',
        'templates/result.html',
        'templates/review.html',
        'static/css/style.css',
        'static/js/exam.js'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ {len(missing_files)} files are missing!")
        return False
    else:
        print(f"\n✅ All {len(required_files)} files exist!")
        return True

def test_database():
    """Test if database exists and has data"""
    print("\n" + "="*60)
    print("Testing Database...")
    print("="*60)
    
    if not os.path.exists('placement_prep.db'):
        print("❌ Database file not found!")
        print("   Run: python init_db.py")
        return False
    
    print("✓ Database file exists")
    
    try:
        from app import app
        from models.database import db, Subject, Question, ExamSession
        
        with app.app_context():
            # Test subjects
            subjects = Subject.query.all()
            print(f"✓ Found {len(subjects)} subjects")
            
            for subject in subjects:
                count = Question.query.filter_by(subject_id=subject.id).count()
                print(f"  - {subject.name}: {count} questions")
            
            # Test total questions
            total_questions = Question.query.count()
            print(f"\n✓ Total questions in database: {total_questions}")
            
            if total_questions == 0:
                print("❌ No questions found in database!")
                print("   Run: python init_db.py")
                return False
            
            # Test question types
            mcq_count = Question.query.filter_by(question_type='mcq').count()
            theory_count = Question.query.filter_by(question_type='theory').count()
            output_count = Question.query.filter_by(question_type='output').count()
            coding_count = Question.query.filter_by(question_type='coding').count()
            
            print(f"\nQuestion Types:")
            print(f"  - MCQ: {mcq_count}")
            print(f"  - Theory: {theory_count}")
            print(f"  - Output: {output_count}")
            print(f"  - Coding: {coding_count}")
            
            print("\n✅ Database is properly configured!")
            return True
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n" + "="*60)
    print("Testing Python Imports...")
    print("="*60)
    
    required_modules = [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'SQLAlchemy'),
        ('docx', 'python-docx'),
    ]
    
    missing_modules = []
    for module_name, display_name in required_modules:
        try:
            __import__(module_name)
            print(f"✓ {display_name}")
        except ImportError:
            print(f"✗ {display_name} - NOT INSTALLED")
            missing_modules.append(display_name)
    
    if missing_modules:
        print(f"\n❌ {len(missing_modules)} modules are missing!")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All required modules are installed!")
        return True

def test_routes():
    """Test if Flask routes are properly configured"""
    print("\n" + "="*60)
    print("Testing Flask Routes...")
    print("="*60)
    
    try:
        from app import app
        
        with app.app_context():
            routes = []
            for rule in app.url_map.iter_rules():
                if rule.endpoint != 'static':
                    routes.append(f"{rule.endpoint}: {rule.rule}")
            
            print(f"✓ Found {len(routes)} routes:")
            for route in sorted(routes):
                print(f"  - {route}")
            
            print("\n✅ Flask routes are properly configured!")
            return True
            
    except Exception as e:
        print(f"❌ Route configuration error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("PLACEMENT PREP APPLICATION - SETUP TEST")
    print("="*60 + "\n")
    
    results = []
    
    # Run tests
    results.append(("File Structure", test_file_structure()))
    results.append(("Python Imports", test_imports()))
    results.append(("Database", test_database()))
    results.append(("Flask Routes", test_routes()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print("\n" + "="*60)
    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print("="*60)
        print("\nYour application is ready to run!")
        print("Start the server with: python app.py")
        print("Then open: http://127.0.0.1:5000")
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total})")
        print("="*60)
        print("\nPlease fix the issues above before running the application.")
    
    print("\n")

if __name__ == '__main__':
    main()
