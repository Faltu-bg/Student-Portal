from flask import Flask
from flask_login import LoginManager
from studentportal.db import db
from studentportal.models import Student,Teacher

def create_app():
    app= Flask(__name__)
    app.secret_key='super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./student.db'

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

    from studentportal.routes import auth_bp,pay_bp

    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(pay_bp,url_prefix='/payment')
    

    return app