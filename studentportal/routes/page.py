from flask import Blueprint,render_template,request,redirect,flash
from studentportal.models import *
from flask_login import login_required,current_user
from studentportal.db import db
from werkzeug.utils import secure_filename
import os
from flask import current_app
import random,string
from datetime import datetime
from werkzeug.security import generate_password_hash


student_bp=Blueprint("student",__name__)

def randompass(length=6):
    characters = string.ascii_letters + string.digits  # Letters and digits
    return ''.join(random.choice(characters) for i in range(length))


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

@student_bp.route("/add-student",methods=["GET", "POST"])
@login_required
def add_student():
    if current_user.role != "teacher":  # Only admins can add students
        return "Unauthorized access", 403

    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        phone = request.form.get("phone")
        addr1 = request.form.get("addr1")
        addr2 = request.form.get("addr2")
        email = request.form.get("email")
        country = request.form.get("country")
        region = request.form.get("region")
        sno = request.form.get("sno")
        sem = request.form.get("sem")
        

        current_year = datetime.now().year
        last_student = Student.query.order_by(Student.sno.desc()).first()  # Get the last student by sno
        last_id = last_student.sno if last_student else 0  # If no students exist, start from 0
        new_id=last_id+1
        sno = f"{current_year}{new_id:04d}"

        random_password = randompass(length=6)
        hashed_password=generate_password_hash(random_password)

        photo = request.files.get("photo")
        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = "default.png"

        new_student = Student(
            name=f"{fname} {lname}",
            phone=phone,
            address=f"{addr1} {addr2}",
            email=email,
            country=country,
            region=region,
            hashed_password=hashed_password,
            photo=filename,
            sno=sno
        )
        db.session.add(new_student)
        db.session.commit()

        flash("Student added successfully!")
        courses = Course.query.filter_by(sem=sem).all()
        for course in courses:
            new_enrollment = Enroll(student_id=new_student.sno, course_id=course.sno)
            db.session.add(new_enrollment)

        db.session.commit()

        flash("Student added and enrolled in respective courses successfully!")
    return render_template("addstudent.html")

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