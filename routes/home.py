from flask import Blueprint, render_template
from models.database import db, Subject, Question

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    """Home page showing all subjects with question counts"""
    subjects_data = []
    
    subjects = Subject.query.all()
    for subject in subjects:
        question_count = Question.query.filter_by(subject_id=subject.id).count()
        subjects_data.append({
            'name': subject.name,
            'count': question_count
        })
    
    return render_template('home.html', subjects=subjects_data)
