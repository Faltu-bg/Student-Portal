from studentportal.db import db

class Course(db.Model):
    __tablename__ = "course"

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    sem = db.Column(db.Integer, nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.sno'), nullable=False)

    teacher = db.relationship('Teacher', back_populates='courses')
    enrollments = db.relationship('Enroll', back_populates='course', cascade="all, delete")
    marks = db.relationship('Marks', back_populates='course', cascade="all, delete")
