from studentportal.db import db
class Payment(db.Model):
    __tablename__ = "payment"

    sno = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.sno'), nullable=False)

    paymentmode = db.Column(db.String(32), nullable=False)
    paymenttype = db.Column(db.String(32), nullable=False)
    referenceid = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(32), nullable=False)

    sem = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    student = db.relationship('Student', back_populates='payments')