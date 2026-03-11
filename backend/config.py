import os

class Config:
    SECRET_KEY = 'ppa-secret-key-saiavinash-2026'
    SQLALCHEMY_DATABASE_URI = "sqlite:///placement.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads', 'resumes')
    MAX_CONTENT_LENGTH = 5*1024*1024
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

    # Redis and Celery Configuration
    REDIS_URL = "redis://localhost:6379/0"
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

