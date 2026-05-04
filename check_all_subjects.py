"""Check all subjects for duplicates and missing answers"""
from app import app
from models.database import db, Subject, Question

def check_subject(subject_name):
    """Check a subject for duplicates and missing answers"""
    print("\n" + "="*80)
    print(f"CHECKING {subject_name.upper()}")
    print("="*80)
    
    subject = Subject.query.filter_by(name=subject_name).first()
    if not subject:
        print(f"Subject '{subject_name}' not found!")
        return
    
    questions = Question.query.filter_by(subject_id=subject.id).all()
    print(f"Total questions: {len(questions)}")
    
    # Check for duplicates
    seen_questions = {}
    duplicates = []
    
    for q in questions:
        q_text = q.question.strip()
        if q_text in seen_questions:
            duplicates.append({
                'question': q_text[:100] + '...' if len(q_text) > 100 else q_text,
                'type': q.question_type,
                'first_id': seen_questions[q_text],
                'duplicate_id': q.id
            })
        else:
            seen_questions[q_text] = q.id
    
    if duplicates:
        print(f"\n⚠️  FOUND {len(duplicates)} DUPLICATE QUESTIONS:")
        for i, dup in enumerate(duplicates[:10], 1):  # Show first 10
            print(f"\n{i}. [{dup['type']}] {dup['question']}")
            print(f"   IDs: {dup['first_id']} and {dup['duplicate_id']}")
        if len(duplicates) > 10:
            print(f"\n... and {len(duplicates) - 10} more duplicates")
    else:
        print("\n✅ No duplicate questions found")
    
    # Check for missing answers
    missing_answers = []
    placeholder_answers = []
    
    for q in questions:
        if not q.answer or q.answer.strip() == '':
            missing_answers.append({
                'id': q.id,
                'type': q.question_type,
                'question': q.question[:100] + '...' if len(q.question) > 100 else q.question
            })
        elif 'refer study material' in q.answer.lower() or 'refer to study material' in q.answer.lower():
            placeholder_answers.append({
                'id': q.id,
                'type': q.question_type,
                'question': q.question[:100] + '...' if len(q.question) > 100 else q.question,
                'answer': q.answer[:100] + '...' if len(q.answer) > 100 else q.answer
            })
    
    if missing_answers:
        print(f"\n⚠️  FOUND {len(missing_answers)} QUESTIONS WITH EMPTY ANSWERS:")
        for i, q in enumerate(missing_answers[:10], 1):
            print(f"\n{i}. [ID: {q['id']}] [{q['type']}] {q['question']}")
        if len(missing_answers) > 10:
            print(f"\n... and {len(missing_answers) - 10} more")
    else:
        print("\n✅ No questions with empty answers")
    
    if placeholder_answers:
        print(f"\n⚠️  FOUND {len(placeholder_answers)} QUESTIONS WITH PLACEHOLDER ANSWERS:")
        for i, q in enumerate(placeholder_answers[:10], 1):
            print(f"\n{i}. [ID: {q['id']}] [{q['type']}] {q['question']}")
            print(f"   Answer: {q['answer']}")
        if len(placeholder_answers) > 10:
            print(f"\n... and {len(placeholder_answers) - 10} more")
    else:
        print("\n✅ No questions with placeholder answers")
    
    # Breakdown by type
    print(f"\n{'='*80}")
    print("BREAKDOWN BY TYPE:")
    print(f"{'='*80}")
    
    types = {}
    for q in questions:
        types[q.question_type] = types.get(q.question_type, 0) + 1
    
    for q_type, count in sorted(types.items()):
        print(f"  {q_type}: {count}")
    
    return {
        'total': len(questions),
        'duplicates': len(duplicates),
        'missing_answers': len(missing_answers),
        'placeholder_answers': len(placeholder_answers)
    }

if __name__ == '__main__':
    with app.app_context():
        print("\n" + "="*80)
        print("CHECKING ALL SUBJECTS FOR DUPLICATES AND MISSING ANSWERS")
        print("="*80)
        
        results = {}
        
        # Check each subject
        for subject_name in ['Java', 'Networks', 'Operating System']:
            results[subject_name] = check_subject(subject_name)
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        total_issues = 0
        for subject_name, stats in results.items():
            issues = stats['duplicates'] + stats['missing_answers'] + stats['placeholder_answers']
            total_issues += issues
            
            status = "✅" if issues == 0 else "⚠️ "
            print(f"\n{status} {subject_name}:")
            print(f"   Total: {stats['total']} questions")
            print(f"   Duplicates: {stats['duplicates']}")
            print(f"   Missing answers: {stats['missing_answers']}")
            print(f"   Placeholder answers: {stats['placeholder_answers']}")
        
        print("\n" + "="*80)
        if total_issues == 0:
            print("✅ ALL SUBJECTS ARE CLEAN - NO ISSUES FOUND!")
        else:
            print(f"⚠️  TOTAL ISSUES FOUND: {total_issues}")
        print("="*80)
