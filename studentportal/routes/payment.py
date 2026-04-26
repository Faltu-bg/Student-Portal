from flask import Blueprint,render_template,request,jsonify
from flask_login import login_required,current_user
from studentportal.models import Payment
from studentportal import db
from razorpay import razorpay

pay_bp=Blueprint("payment",__name__)
client = razorpay.Client(auth=("your-key", "razorpay-key"))

@pay_bp.route("/payment",methods=['GET'])
@login_required
def payment1():
    i=current_user.sno
    pay=Payment.query.filter_by(student_id=i).all()


    sem_status = {}

    for p in pay:
        if p.sem not in sem_status:
            sem_status[p.sem] = "pending"

        if p.status == "success":
            sem_status[p.sem] = "paid"

    return render_template("payment.html",pay=pay,sem_status=sem_status)

@pay_bp.route('/verify_payment', methods=['POST'])
@login_required
def verify_payment():
    data = request.get_json()

    order_id = data.get('razorpay_order_id')
    payment_id = data.get('razorpay_payment_id')
    signature = data.get('razorpay_signature')
    sem = data.get('semester')
    if sem is None:
        return jsonify({"Missing semester"}),400
    sem=int(sem)

    try:
        
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        client.utility.verify_payment_signature(params_dict)

        existing = Payment.query.filter_by(
            student_id=current_user.sno,
            sem=sem,
            status="success"
        ).first()

        if existing:
            return jsonify({"status": "Already paid"}), 400

        
        new_payment = Payment(
            student_id=current_user.sno,
            paymentmode="online",
            paymenttype="semester_fee",
            referenceid=payment_id,
            status="success",
            sem=sem,
            amount=50000
        )

        db.session.add(new_payment)
        db.session.commit()

        return jsonify({"status": "Payment successful"})

    except Exception as e:
        print(e)
        return jsonify({"status": "Verification failed"})
