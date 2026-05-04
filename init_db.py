from app import app
from models.database import db, Subject, Question
from parser.java_parser import parse_java_files
from parser.network_parser import parse_network_files
from parser.os_parser import parse_os_files

def init_database():
    """Initialize database and load all questions"""
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating new tables...")
        db.create_all()
        
        # Create subjects
        print("Creating subjects...")
        subjects = {
            'Java': Subject(name='Java'),
            'Networks': Subject(name='Networks'),
            'Operating System': Subject(name='Operating System')
        }
        
        for subject in subjects.values():
            db.session.add(subject)
        
        db.session.commit()
        print("Subjects created successfully!")
        
        # Parse and load Java questions
        print("\n" + "="*50)
        print("Parsing Java files...")
        print("="*50)
        try:
            java_questions = parse_java_files()
            java_subject = subjects['Java']
            
            for q_data in java_questions:
                question = Question(
                    subject_id=java_subject.id,
                    question_type=q_data['question_type'],
                    question=q_data['question'],
                    option_a=q_data['option_a'],
                    option_b=q_data['option_b'],
                    option_c=q_data['option_c'],
                    option_d=q_data['option_d'],
                    answer=q_data['answer'],
                    explanation=q_data['explanation'],
                    topic=q_data['topic']
                )
                db.session.add(question)
            
            db.session.commit()
            print(f"✓ Loaded {len(java_questions)} Java questions")
        except Exception as e:
            print(f"✗ Error loading Java questions: {e}")
            db.session.rollback()
        
        # Parse and load Network questions
        print("\n" + "="*50)
        print("Parsing Network files...")
        print("="*50)
        try:
            network_questions = parse_network_files()
            network_subject = subjects['Networks']
            
            for q_data in network_questions:
                question = Question(
                    subject_id=network_subject.id,
                    question_type=q_data['question_type'],
                    question=q_data['question'],
                    option_a=q_data['option_a'],
                    option_b=q_data['option_b'],
                    option_c=q_data['option_c'],
                    option_d=q_data['option_d'],
                    answer=q_data['answer'],
                    explanation=q_data['explanation'],
                    topic=q_data['topic']
                )
                db.session.add(question)
            
            db.session.commit()
            print(f"✓ Loaded {len(network_questions)} Network questions")
        except Exception as e:
            print(f"✗ Error loading Network questions: {e}")
            db.session.rollback()
        
        # Parse and load OS questions
        print("\n" + "="*50)
        print("Parsing OS files...")
        print("="*50)
        try:
            os_questions = parse_os_files()
            os_subject = subjects['Operating System']
            
            for q_data in os_questions:
                question = Question(
                    subject_id=os_subject.id,
                    question_type=q_data['question_type'],
                    question=q_data['question'],
                    option_a=q_data['option_a'],
                    option_b=q_data['option_b'],
                    option_c=q_data['option_c'],
                    option_d=q_data['option_d'],
                    answer=q_data['answer'],
                    explanation=q_data['explanation'],
                    topic=q_data['topic']
                )
                db.session.add(question)
            
            db.session.commit()
            print(f"✓ Loaded {len(os_questions)} OS questions")
        except Exception as e:
            print(f"✗ Error loading OS questions: {e}")
            db.session.rollback()
        
        # Print summary
        print("\n" + "="*50)
        print("DATABASE INITIALIZATION COMPLETE")
        print("="*50)
        
        for subject_name, subject_obj in subjects.items():
            count = Question.query.filter_by(subject_id=subject_obj.id).count()
            print(f"{subject_name}: {count} questions")
        
        total = Question.query.count()
        print(f"\nTotal: {total} questions loaded successfully!")

if __name__ == '__main__':
    init_database()
