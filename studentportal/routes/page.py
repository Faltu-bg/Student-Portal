from flask import Blueprint,render_template,request,redirect,flash
from studentportal.models import *
from flask_login import login_required,current_user
from studentportal.db import db
from werkzeug.utils import secure_filename
import os
from flask import current_app


student_bp=Blueprint("student",__name__)

@student_bp.route("/")
@login_required
def home():
    student = Student.query.get(current_user.sno)
    enrollments = Enroll.query.filter_by(student_id=student.sno).all()
    marks = Marks.query.filter_by(student_id=student.sno).all()
    payments = Payment.query.filter_by(student_id=student.sno).all()
    sem_status = {}

    for p in payments:
        if p.sem not in sem_status:
            sem_status[p.sem] = "pending"

        if p.status == "success":
            sem_status[p.sem] = "paid"
    avg_marks = 0
    if marks:
        avg_marks = sum(
            (m.intmarks or 0) + (m.extmarks or 0) + (m.midmarks or 0)
            for m in marks
        ) / len(marks)

    return render_template(
        "home.html",
        student=student,
        enrollments=enrollments,
        marks=marks,
        sem_status=sem_status,
        payments=payments,
        avg_marks=avg_marks
    )


@student_bp.route("/result")
@login_required
def result():

    student_id = current_user.sno
    selected_sem = request.args.get("sem", type=int)

    student = Student.query.get(student_id)

    query = db.session.query(Marks, Course).join(Course).filter(
        Marks.student_id == student_id
    )

    if selected_sem:
        query = query.filter(Course.sem == selected_sem)

    marks_data = query.all()

    all_sems = db.session.query(Course.sem).distinct().all()
    all_sems = sorted([s[0] for s in all_sems])

    return render_template(
        "result.html",
        student=student,
        marks_data=marks_data,
        sems=all_sems,
        selected_sem=selected_sem
    )

@student_bp.route("/profile", methods=['GET','POST'])
def profile():

    if request.method=='POST':
        file = request.files.get("photo")
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            current_user.photo = filename
        current_user.name = request.form.get("fname")
        current_user.phone = request.form.get("phone")
        current_user.address = request.form.get("addr1")
        current_user.email = request.form.get("email")
        current_user.country = request.form.get("country")
        current_user.region = request.form.get("region")

        db.session.commit()
        flash("Profile updated successfully")
        return redirect("/profile")
    return render_template("profile.html")    

@student_bp.route("/password")
def password():

    return render_template("passwordpage.html")