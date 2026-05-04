from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    questions = db.relationship('Question', backref='subject', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subject {self.name}>'


class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # mcq, theory, output, coding
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.Text, nullable=True)
    option_b = db.Column(db.Text, nullable=True)
    option_c = db.Column(db.Text, nullable=True)
    option_d = db.Column(db.Text, nullable=True)
    answer = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    topic = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question[:50]}...>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject.name,
            'question_type': self.question_type,
            'question': self.question,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'answer': self.answer,
            'explanation': self.explanation,
            'topic': self.topic
        }


class ExamSession(db.Model):
    __tablename__ = 'exam_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    answers = db.relationship('ExamAnswer', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ExamSession {self.id}: {self.student_name} - {self.subject}>'


class ExamAnswer(db.Model):
    __tablename__ = 'exam_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('exam_sessions.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_answer = db.Column(db.Text, nullable=True)
    is_correct = db.Column(db.Boolean, nullable=False)
    question = db.relationship('Question', backref='exam_answers', lazy=True)
    
    def __repr__(self):
        return f'<ExamAnswer {self.id}: Q{self.question_id} - {"Correct" if self.is_correct else "Wrong"}>'
