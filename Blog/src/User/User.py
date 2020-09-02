from flask.views import View
from flask import render_template, flash, redirect, request, url_for, session
from Blog.src.User.Model import User as UserModel, db
from functools import wraps
import bcrypt

def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session or 'user' in session and not session['user']['authenticated']:
            return redirect(url_for('UserAdminLogin'))
        return func(*args, **kwargs)
    return wrapper

def user_exists(username) -> bool:
    user = db.session.query(UserModel).filter(UserModel.username==username).first()
    return True if user else False

def get_user_id() -> int:
    return session['user']['id'] if 'user' in session and session['user']['id'] else 0

class UserAdmin(View):
    @is_authenticated
    def dispatch_request(self):
        users = db.session.query(UserModel).order_by(UserModel.id.desc()).all()
        return render_template('admin/user/index.html', title='Users', users=users)


class UserAdminAdd(View):

    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if not username or not password:
                flash('Please enter username and password', 'error')
                return redirect(url_for(request.endpoint))

            password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            username = username.lower()
            try:
                if user_exists(username):
                    flash('User already exists', 'error')
                    return redirect(url_for(request.endpoint))

                db.session.add(
                    UserModel(
                        username=username,
                        password=password
                    )
                )
                db.session.commit()
                flash('User created', 'success')
                return redirect(url_for('UserAdmin'))
            except(Exception) as error:
                flash(str(error), 'error')
                return redirect(url_for(request.endpoint))

        return render_template('admin/user/form.html', title='Users', submit_tag='Create')


class UserAdminLogin(View):
    
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            if not username or not password:
                flash('Please enter username and password', 'error')
                return redirect(url_for(request.endpoint))

            # Find user
            user_found = False
            user = db.session.query(UserModel).filter(UserModel.username==username).first()
            if user:
                valid = bcrypt.checkpw(password.encode(), user.password.encode())
                if valid:
                    user_found = True
                    session['user'] = {
                        'authenticated': True,
                        'name': username,
                        'id': user.id
                    }
                    
            if user_found:
                return redirect(url_for('PostAdmin'))
            else:
                flash('User not found', 'error')
                return redirect(url_for('UserAdminLogin'))

        return render_template('admin/user/login.html')


class UserAdminLogout(View):
    def dispatch_request(self):
        if 'user' in session:
            del session['user']
        return redirect(url_for('UserAdminLogin'))
