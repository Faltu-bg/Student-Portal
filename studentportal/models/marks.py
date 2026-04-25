from studentportal.db import db

class Marks(db.Model):
    __tablename__ = "marks"

    sno = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.sno'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.sno'), nullable=False)

    intmarks = db.Column(db.Integer)
    extmarks = db.Column(db.Integer)
    midmarks = db.Column(db.Integer)

    student = db.relationship('Student', back_populates='marks')
    course = db.relationship('Course', back_populates='marks')