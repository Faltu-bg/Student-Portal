from studentportal.db import db

class Enroll(db.Model):
    __tablename__ = "enroll"

    sno = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.sno'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.sno'), nullable=False)

    marks = db.Column(db.Integer)

    student = db.relationship('Student', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')

    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),
    )