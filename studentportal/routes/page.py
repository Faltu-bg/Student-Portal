from flask import Blueprint,render_template
from studentportal.models import *
from flask_login import login_required,current_user
from studentportal.db import db

student_bp=Blueprint("student",__name__)

@student_bp.route("/")
@login_required
def home():
   
    return render_template("home.html")

@student_bp.route("/result")
@login_required
def result():
    student_id = current_user.sno

    student = Student.query.get(student_id)
    if not student:
        return "Student not found", 404

    marks_data = db.session.query(Marks, Course).join(Course).filter(
        Marks.student_id == student_id
    ).all()

    sems = sorted({course.sem for _, course in marks_data})

    return render_template(
        "result.html",
        student=student,
        marks_data=marks_data,
        sems=sems
    )