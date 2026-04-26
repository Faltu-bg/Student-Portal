from studentportal.db import db
from flask_login import UserMixin


class Student(db.Model, UserMixin):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    hashed_password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50))
    date = db.Column(db.String(12))

    enrollments = db.relationship('Enroll', back_populates='student', cascade="all, delete")
    payments = db.relationship('Payment', back_populates='student', cascade="all, delete")
    marks = db.relationship('Marks', back_populates='student', cascade="all, delete")

    def get_id(self):
        return f"student-{self.sno}"
