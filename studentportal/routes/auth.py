from flask import Blueprint,request,flash,redirect,render_template
from flask_login import login_required,logout_user,login_user
from studentportal.models import Student,Teacher

auth_bp=Blueprint("auth",__name__)

@auth_bp.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user=Student.query.filter_by(sno=username).first()
        if not user:
            user=Teacher.query.filter_by(name=username).first()
        if user:
            if password == user.hashed_password:
                login_user(user)
                return redirect("/home")
            else:

                flash('Wrong Password')
        else:

            print("User not found")
    return render_template("login.html")

@auth_bp.route("/logout",methods=['GET'])
@login_required
def logout():
    logout_user()
    print("successfull")