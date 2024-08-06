from flask import Blueprint,render_template,request,flash,redirect,url_for,make_response
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user
from .models import Admin
from flask_wtf.csrf import CSRFProtect
from functools import wraps
auth = Blueprint('auth', __name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('admin')  
        password = request.form.get('password')

        admin = Admin.query.filter_by(admin_name=name).first()
        if admin:
            if check_password_hash(admin.password, password):
                login_user(admin, remember=True)
                return redirect(url_for('views.showDashboard'))
            else:
                flash('Incorrect password, try again.', category='error')   
        else:
            flash('Admin does not exist.', category='error')
    return render_template('authentication/login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get("password")
        new_admin = Admin(admin_name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('authentication/sign_up.html')