from flask import Blueprint,request,render_template,flash
from studentportal.db import db
from studentportal.models import *
from flask_login import login_required,logout_user,login_user,current_user

marks_bp=Blueprint("Marks",__name__)

@marks_bp.route("/add-marks", methods=["GET", "POST"])
@login_required
def add_marks():
    if current_user.role!="teacher":
        return "unauthorized access",403
    students = Student.query.all()
    selected_student = None
    enrollments = []
    marks_map = {}

    student_id = request.values.get("student_id")
    selected_sem = request.values.get("sem", type=int)

    if student_id:
        selected_student = Student.query.get(student_id)

        # 👇 filter enrollments by semester (IMPORTANT)
        query = Enroll.query.filter_by(student_id=student_id)

        if selected_sem:
            query = query.join(Course).filter(Course.sem == selected_sem)

        enrollments = query.all()

        # load marks
        marks_list = Marks.query.filter_by(student_id=student_id).all()
        marks_map = {m.course_id: m for m in marks_list}

    if request.method == "POST":
        for e in enrollments:
            course_id = e.course_id

            intmarks = request.form.get(f"int_{course_id}")
            midmarks = request.form.get(f"mid_{course_id}")
            extmarks = request.form.get(f"ext_{course_id}")

            marks = Marks.query.filter_by(
                student_id=student_id,
                course_id=course_id
            ).first()

            if marks:
                marks.intmarks = intmarks
                marks.midmarks = midmarks
                marks.extmarks = extmarks
            else:
                db.session.add(Marks(
                    student_id=student_id,
                    course_id=course_id,
                    intmarks=intmarks,
                    midmarks=midmarks,
                    extmarks=extmarks
                ))

        db.session.commit()
        flash("Marks updated")

    return render_template(
        "addmarks.html",
        students=students,
        selected_student=selected_student,
        enrollments=enrollments,
        marks_map=marks_map,
        selected_sem=selected_sem
    )