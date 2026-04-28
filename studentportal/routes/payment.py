from flask import Blueprint,render_template,request,jsonify
from flask_login import login_required,current_user
from studentportal.models import *
from studentportal import db
import razorpay
from studentportal.fees import is_fees_paid


pay_bp=Blueprint("payment",__name__)
client = razorpay.Client(auth=("your-key", "razorpay-key"))

@pay_bp.route("/payment",methods=['GET'])
@login_required
def payment1():
    i=current_user.sno
    pay=Payment.query.filter_by(student_id=i).all()


    sem_status = {}
    sem_payment={}
    for p in pay:
        if p.sem not in sem_status:
            sem_status[p.sem] = "pending"

        if p.status == "success":
            sem_status[p.sem] = "paid"
            sem_payment[p.sem] = p

    return render_template(
        "payment.html",
        pay=pay,
        sem_status=sem_status,
        sem_payment=sem_payment
        )


@pay_bp.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    sem = data['semester']

    amount = 50000  # or vary by semester

    order_data = {
        "amount": amount,
        "currency": "INR",
        "receipt": f"sem_{sem}"
    }

    order = client.order.create(data=order_data)

    return jsonify({
        "order_id": order['id'],
        "amount": amount,
        "key": "key"
    })

@pay_bp.route('/verify_payment', methods=['POST'])
@login_required
def verify_payment():
    data = request.get_json()

    order_id = data.get('razorpay_order_id')
    payment_id = data.get('razorpay_payment_id')
    signature = data.get('razorpay_signature')
    sem = data.get('semester')
    if sem is None:
        return jsonify({"error": "Missing semester"}), 400
    sem=int(sem)

    try:
        
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        client.utility.verify_payment_signature(params_dict)

        if is_fees_paid(current_user.sno, sem):
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


@pay_bp.route("/download_receipt/<int:receipt>")
def download_receipt(receipt):
    print(f"{receipt}")
    user=current_user.sno
    student = Student.query.get(user)
    payment=Payment.query.filter_by(student_id=user, sno=receipt).first()
    if not payment:
        return "Unauthorized or receipt not found", 404

    return render_template("receipt.html",student=student,payment=payment)