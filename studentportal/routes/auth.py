from flask import Blueprint,request,flash,redirect,render_template
from flask_login import login_required,logout_user,login_user,current_user
from studentportal.models import *
from studentportal import db

auth_bp=Blueprint("auth",__name__)

@auth_bp.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get("username")
        password = request.form.get("password")
        print("FORM DATA:", request.form)
        print("USERNAME:", username)
        print("PASSWORD:", password)
        user=Student.query.filter_by(sno=username).first()
        if not user:
            user=Teacher.query.filter_by(name=username).first()
       
        if user:
            if password == user.hashed_password:
                login_user(user)
                print(f"Logged in user: {user}")
                return redirect("/")
            else:

                flash('Invalid Credentials')
        else:

            print("User not found")
    return render_template("login.html")


@auth_bp.route("/change-password",methods=['POST'])
@login_required
def changepass():
    old_password=request.form.get("old_password")
    new_password=request.form.get("new_password")
    confirm_password=request.form.get("confirm_password")

    if old_password == current_user.hashed_password:
        if new_password==confirm_password:
            
            current_user.hashed_password = new_password
            db.session.commit()
            flash("Password change successfully")
            return redirect("/password")
        else:
            flash("New passwords do not match")
            
    else:    
        flash("Old password is incorrect")

    return redirect("/password")


@auth_bp.route("/logout",methods=['GET'])
@login_required
def logout():
    logout_user()
    print("successfull")
    return redirect("/auth/login")