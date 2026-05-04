from flask import Flask
from config import Config
from models.database import db

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from routes.home import home_bp
    from routes.study import study_bp
    from routes.exam import exam_bp
    from routes.results import results_bp
    
    app.register_blueprint(home_bp)
    app.register_blueprint(study_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(results_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
