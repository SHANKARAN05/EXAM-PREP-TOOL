"""
Test script to verify parsers are working correctly
"""

import os
from parser.java_parser import parse_java_files

def test_java_parsers():
    """Test Java file parsing"""
    print("="*60)
    print("Testing Java Parsers...")
    print("="*60)
    
    questions = parse_java_files()
    
    print(f"\nTotal questions parsed: {len(questions)}")
    
    # Count by type
    mcq_count = sum(1 for q in questions if q['question_type'] == 'mcq')
    theory_count = sum(1 for q in questions if q['question_type'] == 'theory')
    output_count = sum(1 for q in questions if q['question_type'] == 'output')
    coding_count = sum(1 for q in questions if q['question_type'] == 'coding')
    
    print(f"\nBreakdown by type:")
    print(f"  MCQ: {mcq_count}")
    print(f"  Theory: {theory_count}")
    print(f"  Output: {output_count}")
    print(f"  Coding: {coding_count}")
    
    # Count by topic
    topics = {}
    for q in questions:
        topic = q['topic']
        topics[topic] = topics.get(topic, 0) + 1
    
    print(f"\nBreakdown by topic:")
    for topic, count in sorted(topics.items()):
        print(f"  {topic}: {count}")
    
    # Show sample questions
    print(f"\n{'='*60}")
    print("Sample Questions:")
    print("="*60)
    
    # Sample MCQ
    mcq_samples = [q for q in questions if q['question_type'] == 'mcq']
    if mcq_samples:
        print("\n[MCQ Sample]")
        q = mcq_samples[0]
        print(f"Question: {q['question']}")
        print(f"A) {q['option_a']}")
        print(f"B) {q['option_b']}")
        print(f"C) {q['option_c']}")
        print(f"D) {q['option_d']}")
        print(f"Answer: {q['answer']}")
        print(f"Explanation: {q['explanation']}")
    
    # Sample Theory
    theory_samples = [q for q in questions if q['question_type'] == 'theory']
    if theory_samples:
        print("\n[Theory Sample]")
        q = theory_samples[0]
        print(f"Question: {q['question']}")
        print(f"Answer: {q['answer'][:200]}...")  # First 200 chars
    
    # Sample Output
    output_samples = [q for q in questions if q['question_type'] == 'output']
    if output_samples:
        print("\n[Output Sample]")
        q = output_samples[0]
        print(f"Question: {q['question'][:200]}...")
        print(f"Answer: {q['answer']}")
    
    # Sample Coding
    coding_samples = [q for q in questions if q['question_type'] == 'coding']
    if coding_samples:
        print("\n[Coding Sample]")
        q = coding_samples[0]
        print(f"Question: {q['question']}")
        print(f"Answer: {q['answer'][:200]}...")
    
    # Check for "Refer study material" answers
    refer_count = sum(1 for q in questions if 'refer' in q['answer'].lower() and 'material' in q['answer'].lower())
    print(f"\n{'='*60}")
    print(f"Questions with 'Refer study material': {refer_count}")
    
    if refer_count > 0:
        print("\n⚠️  WARNING: Some questions still have placeholder answers!")
        print("These questions need proper answers:")
        for q in questions:
            if 'refer' in q['answer'].lower() and 'material' in q['answer'].lower():
                print(f"  - [{q['question_type']}] {q['question'][:80]}...")
    else:
        print("\n✅ All questions have proper answers!")
    
    print("\n" + "="*60)
    print("Java Parser Test Complete!")
    print("="*60)

if __name__ == '__main__':
    test_java_parsers()
