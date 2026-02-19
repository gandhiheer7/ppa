import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, send_from_directory
from config import Config
from extensions import db, jwt, cors, cache, celery_app
from models import create_admin_if_not_exists

from utils.error_handlers import register_error_handlers
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import student_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure directories exist
    os.makedirs(os.path.join(app.config['BASE_DIR'], 'instance'), exist_ok=True)
    os.makedirs(os.path.join(app.config['BASE_DIR'], 'uploads'), exist_ok=True)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    cache.init_app(app)

    # Initialize Celery Configuration
    celery_app.conf.update(app.config.get('CELERY_CONFIG', {}))
    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app.Task = ContextTask

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)

    register_error_handlers(app)

    # --- NEW: Route to serve uploaded resumes ---
    @app.route('/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        upload_dir = os.path.join(app.config['BASE_DIR'], 'uploads')
        return send_from_directory(upload_dir, filename)

    with app.app_context():
        db.create_all()
        create_admin_if_not_exists()

    if not app.debug:
        file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=5)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()