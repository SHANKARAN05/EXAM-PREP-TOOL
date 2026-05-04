"""Check what's actually in the database"""
from app import app
from models.database import db, Question, Subject

with app.app_context():
    # Get Java subject
    java_subject = Subject.query.filter_by(name='Java').first()
    
    if java_subject:
        # Get some theory questions
        theory_questions = Question.query.filter_by(
            subject_id=java_subject.id,
            question_type='theory'
        ).limit(10).all()
        
        print("="*80)
        print("THEORY QUESTIONS SAMPLE:")
        print("="*80)
        for q in theory_questions:
            print(f"\nQuestion: {q.question}")
            print(f"Answer: {q.answer[:200]}...")
            print("-"*80)
        
        # Get output questions
        output_questions = Question.query.filter_by(
            subject_id=java_subject.id,
            question_type='output'
        ).all()
        
        print("\n" + "="*80)
        print(f"OUTPUT QUESTIONS ({len(output_questions)} total):")
        print("="*80)
        for q in output_questions:
            print(f"\nQuestion: {q.question[:100]}...")
            print(f"Answer: {q.answer}")
            print("-"*80)
        
        # Get coding questions
        coding_questions = Question.query.filter_by(
            subject_id=java_subject.id,
            question_type='coding'
        ).all()
        
        print("\n" + "="*80)
        print(f"CODING QUESTIONS ({len(coding_questions)} total):")
        print("="*80)
        for q in coding_questions:
            print(f"\nQuestion: {q.question}")
            print(f"Answer: {q.answer[:300]}...")
            print("-"*80)
