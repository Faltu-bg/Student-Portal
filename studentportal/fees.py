from studentportal.models import Payment

def is_fees_paid(student_id, sem):
        payment = Payment.query.filter_by(
        student_id=student_id,
        sem=sem,
        status="success"
        ).first()

        return payment is not None 