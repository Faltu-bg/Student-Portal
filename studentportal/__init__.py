from flask import Flask
from flask_login import LoginManager
from studentportal.db import db
from studentportal.models import *
import os

def create_app():
    template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
    app= Flask(__name__,template_folder=template_path,static_folder="static")
    app.secret_key='super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./student.db'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    db.init_app(app)
    logman=LoginManager()
    logman.init_app(app)
    logman.login_view="auth.login"

    @logman.user_loader
    def load_user(user_id):
        try:
            role, id = user_id.split("-")
        except ValueError:
            return None

        if role == "student":
            return Student.query.get(int(id))
        elif role == "teacher":
            return Teacher.query.get(int(id))

        return None

    from studentportal.routes import auth_bp,pay_bp,student_bp

    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(pay_bp,url_prefix='/payment')
    app.register_blueprint(student_bp)

    return app