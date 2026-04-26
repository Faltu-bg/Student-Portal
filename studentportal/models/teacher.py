from studentportal.db import db
from flask_login import UserMixin

class Teacher(db.Model, UserMixin):
    __tablename__ = "teacher"

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    hashed_password = db.Column(db.String(60), nullable=False)

    courses = db.relationship('Course', back_populates='teacher', cascade="all, delete")

    def get_id(self):
        return f"teacher-{self.sno}"
