from flask import Blueprint, render_template
from models.database import db, ExamSession, ExamAnswer, Question, Subject

results_bp = Blueprint('results', __name__)

@results_bp.route('/result/<int:session_id>')
def show_result(session_id):
    """Show exam result"""
    exam_session = ExamSession.query.get_or_404(session_id)
    
    # Get subject breakdown for combined exam
    subject_breakdown = {}
    if exam_session.subject == 'Combined':
        exam_answers = ExamAnswer.query.filter_by(session_id=session_id).all()
        
        for exam_answer in exam_answers:
            subject_name = exam_answer.question.subject.name
            if subject_name not in subject_breakdown:
                subject_breakdown[subject_name] = {'correct': 0, 'total': 0}
            
            subject_breakdown[subject_name]['total'] += 1
            if exam_answer.is_correct:
                subject_breakdown[subject_name]['correct'] += 1
    
    percentage = (exam_session.score / exam_session.total * 100) if exam_session.total > 0 else 0
    
    return render_template('result.html',
                         session=exam_session,
                         percentage=percentage,
                         subject_breakdown=subject_breakdown)


@results_bp.route('/review/<int:session_id>')
def review_answers(session_id):
    """Review wrong answers"""
    exam_session = ExamSession.query.get_or_404(session_id)
    
    # Get all answers with questions
    exam_answers = ExamAnswer.query.filter_by(session_id=session_id).all()
    
    # Separate correct and wrong answers
    wrong_answers = []
    correct_answers = []
    
    for exam_answer in exam_answers:
        answer_data = {
            'question': exam_answer.question,
            'selected_answer': exam_answer.selected_answer,
            'is_correct': exam_answer.is_correct
        }
        
        if exam_answer.is_correct:
            correct_answers.append(answer_data)
        else:
            wrong_answers.append(answer_data)
    
    return render_template('review.html',
                         session=exam_session,
                         wrong_answers=wrong_answers,
                         correct_answers=correct_answers)
