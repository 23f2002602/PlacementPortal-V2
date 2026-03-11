import os
from flask import Flask, send_from_directory
from config import Config
from models import db
from models.models import User
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from extensions import cache

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

def create_app():
    app = Flask(__name__)

    CORS(app)
    
    app.config.from_object(Config)

    db.init_app(app)
    cache.init_app(app, config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': Config.REDIS_URL})

    from routes.auth_routes    import auth_bp
    from routes.admin_routes  import admin_bp
    from routes.company_routes import company_bp
    from routes.student_routes import student_bp

    app.register_blueprint(auth_bp,    url_prefix='/api')
    app.register_blueprint(admin_bp,   url_prefix='/api/admin')
    app.register_blueprint(company_bp, url_prefix='/api/company')
    app.register_blueprint(student_bp, url_prefix='/api/student')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        file_path = os.path.join(FRONTEND_DIR, path)
        if path and os.path.isfile(file_path):
            return send_from_directory(FRONTEND_DIR, path)
        return send_from_directory(FRONTEND_DIR, 'index.html')

    @app.route('/api')
    def home():
        return {"message": "Placement Portal API is running !"}
    
    @app.route("/api/admin")
    def admin():
        return {"message": "Admin route is working !!"}
    
    def seed_admin():
    # Create the admin user only if it doesn't already exist
        if not User.query.filter_by(role='admin').first():
            admin = User(
                name     = 'Admin',
                email    = 'admin@ppa.com',
                password = generate_password_hash('admin'),
                role     = 'admin'
            )
            db.session.add(admin)
            db.session.commit()
            print('Admin created → admin@ppa.com / admin')

    with app.app_context():
        db.create_all()
        seed_admin()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
