from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from models.database import db, Subject, Question, ExamSession, ExamAnswer
from sqlalchemy import func
import random

exam_bp = Blueprint('exam', __name__)

@exam_bp.route('/exam/<subject>')
def exam_setup(subject):
    """Exam setup page"""
    if subject == 'Combined':
        return render_template('exam.html', subject='Combined', is_setup=True)
    
    # Verify subject exists
    subject_obj = Subject.query.filter_by(name=subject).first_or_404()
    return render_template('exam.html', subject=subject, is_setup=True)


@exam_bp.route('/exam/<subject>/start', methods=['POST'])
def start_exam(subject):
    """Start exam and load questions"""
    student_name = request.form.get('student_name', 'Anonymous')
    question_count = int(request.form.get('question_count', 10))
    
    # Store in session
    session['student_name'] = student_name
    session['exam_subject'] = subject
    session['question_count'] = question_count
    
    # Load questions
    if subject == 'Combined':
        # Get equal questions from all subjects
        questions_per_subject = question_count // 3
        remainder = question_count % 3
        
        all_questions = []
        subjects = Subject.query.all()
        
        for i, subj in enumerate(subjects):
            count = questions_per_subject + (1 if i < remainder else 0)
            questions = Question.query.filter_by(subject_id=subj.id).order_by(func.random()).limit(count).all()
            all_questions.extend(questions)
        
        # Shuffle combined questions
        random.shuffle(all_questions)
    else:
        # Get questions for specific subject
        subject_obj = Subject.query.filter_by(name=subject).first_or_404()
        all_questions = Question.query.filter_by(subject_id=subject_obj.id).order_by(func.random()).limit(question_count).all()
    
    # Store question IDs in session
    session['exam_questions'] = [q.id for q in all_questions]
    session['current_question_index'] = 0
    session['exam_answers'] = {}
    
    return redirect(url_for('exam.take_exam'))


@exam_bp.route('/exam/take')
def take_exam():
    """Take exam page"""
    if 'exam_questions' not in session:
        return redirect(url_for('home.index'))
    
    question_ids = session['exam_questions']
    current_index = session.get('current_question_index', 0)
    
    if current_index >= len(question_ids):
        return redirect(url_for('exam.submit_exam'))
    
    # Get current question
    question_id = question_ids[current_index]
    question = Question.query.get_or_404(question_id)
    
    # Get previously selected answer if any
    selected_answer = session.get('exam_answers', {}).get(str(question_id), '')
    
    total_questions = len(question_ids)
    time_limit = total_questions * 60  # 1 minute per question
    
    return render_template('exam.html',
                         subject=session['exam_subject'],
                         question=question,
                         current_index=current_index,
                         total_questions=total_questions,
                         time_limit=time_limit,
                         selected_answer=selected_answer,
                         is_setup=False)


@exam_bp.route('/exam/answer', methods=['POST'])
def save_answer():
    """Save answer and navigate"""
    data = request.get_json()
    question_id = data.get('question_id')
    answer = data.get('answer', '')
    action = data.get('action', 'next')
    
    # Save answer in session
    if 'exam_answers' not in session:
        session['exam_answers'] = {}
    
    exam_answers = session['exam_answers']
    exam_answers[str(question_id)] = answer
    session['exam_answers'] = exam_answers
    
    # Update current index
    current_index = session.get('current_question_index', 0)
    
    if action == 'next':
        current_index += 1
    elif action == 'previous':
        current_index = max(0, current_index - 1)
    
    session['current_question_index'] = current_index
    
    # Check if exam is complete
    question_ids = session['exam_questions']
    if current_index >= len(question_ids):
        return jsonify({'redirect': url_for('exam.submit_exam')})
    
    return jsonify({'success': True, 'redirect': url_for('exam.take_exam')})


@exam_bp.route('/exam/submit', methods=['GET', 'POST'])
def submit_exam():
    """Submit exam and calculate score by comparing all answers"""
    if 'exam_questions' not in session:
        return redirect(url_for('home.index'))
    
    question_ids = session['exam_questions']
    exam_answers = session.get('exam_answers', {})
    student_name = session.get('student_name', 'Anonymous')
    subject = session.get('exam_subject', 'Unknown')
    
    # Calculate score by comparing student answers with correct answers
    score = 0
    total = len(question_ids)
    
    # Create exam session
    exam_session = ExamSession(
        student_name=student_name,
        subject=subject,
        score=0,  # Will update after checking all answers
        total=total
    )
    db.session.add(exam_session)
    db.session.flush()  # Get session ID
    
    # Check each answer by comparing with the resource answer
    for question_id in question_ids:
        question = Question.query.get(question_id)
        selected_answer = exam_answers.get(str(question_id), '').strip()
        
        # Compare student answer with correct answer from resource
        is_correct = False
        
        if question.question_type == 'mcq':
            # For MCQ, compare the selected option letter
            correct_answer = question.answer.strip().upper()
            student_answer = selected_answer.upper()
            is_correct = (student_answer == correct_answer)
            
            if is_correct:
                score += 1
        
        elif question.question_type in ['theory', 'output', 'coding']:
            # For theory/output/coding, mark as correct if student provided an answer
            # (Manual evaluation would be needed for actual correctness)
            # For now, we just check if they attempted it
            if selected_answer:
                # You can add more sophisticated comparison here
                # For output questions, we can do exact match
                if question.question_type == 'output':
                    # Try exact match for output questions
                    correct_output = question.answer.strip()
                    if selected_answer.lower() == correct_output.lower():
                        is_correct = True
                        score += 1
                else:
                    # For theory and coding, mark as attempted (not auto-graded)
                    is_correct = False  # Requires manual review
        
        # Save exam answer with comparison result
        exam_answer = ExamAnswer(
            session_id=exam_session.id,
            question_id=question_id,
            selected_answer=selected_answer,
            is_correct=is_correct
        )
        db.session.add(exam_answer)
    
    # Update final score after comparing all answers
    exam_session.score = score
    db.session.commit()
    
    # Clear session data
    session.pop('exam_questions', None)
    session.pop('exam_answers', None)
    session.pop('current_question_index', None)
    session.pop('student_name', None)
    session.pop('exam_subject', None)
    session.pop('question_count', None)
    
    return redirect(url_for('results.show_result', session_id=exam_session.id))


@exam_bp.route('/api/questions/<subject>')
def get_questions_api(subject):
    """API endpoint to get questions for a subject"""
    if subject == 'Combined':
        questions = Question.query.all()
    else:
        subject_obj = Subject.query.filter_by(name=subject).first_or_404()
        questions = Question.query.filter_by(subject_id=subject_obj.id).all()
    
    return jsonify([q.to_dict() for q in questions])
