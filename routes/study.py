from flask import Blueprint, render_template, request
from models.database import db, Subject, Question
from sqlalchemy import func

study_bp = Blueprint('study', __name__)

@study_bp.route('/study/<subject>')
def study_mode(subject):
    """Study mode for a specific subject"""
    # Get subject from database
    subject_obj = Subject.query.filter_by(name=subject).first_or_404()
    
    # Get filter parameters
    topic = request.args.get('topic', '')
    question_type = request.args.get('type', '')
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    
    # Build query
    query = Question.query.filter_by(subject_id=subject_obj.id)
    
    if topic:
        query = query.filter_by(topic=topic)
    
    if question_type:
        query = query.filter_by(question_type=question_type)
    
    if search:
        query = query.filter(Question.question.like(f'%{search}%'))
    
    # Paginate
    per_page = 20
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    questions = pagination.items
    
    # Get all topics for filter dropdown
    topics = db.session.query(Question.topic).filter_by(subject_id=subject_obj.id).distinct().all()
    topics = [t[0] for t in topics]
    
    # Get question types for filter
    question_types = db.session.query(Question.question_type).filter_by(subject_id=subject_obj.id).distinct().all()
    question_types = [qt[0] for qt in question_types]
    
    return render_template('study.html',
                         subject=subject,
                         questions=questions,
                         topics=topics,
                         question_types=question_types,
                         pagination=pagination,
                         current_topic=topic,
                         current_type=question_type,
                         search_query=search)
