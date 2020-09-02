from Blog.app import app, run_migration
from flask import render_template

# Migration status
run_migration()

# Load controllers

# Post Controller
from Blog.src.Post.Post import *

# Client side
app.add_url_rule('/', view_func=Post.as_view('PostHome'))
app.add_url_rule('/view/<int:id>', view_func=PostView.as_view('PostView'))

# Admin side
app.add_url_rule('/admin/post', view_func=PostAdmin.as_view('PostAdmin'))
app.add_url_rule('/admin/post/add', view_func=PostAdminAdd.as_view('PostAdminAdd'))


# User Controller
from Blog.src.User.User import *

# Admin side
app.add_url_rule('/admin/user', view_func=UserAdmin.as_view('UserAdmin'))
app.add_url_rule('/admin/user/add', view_func=UserAdminAdd.as_view('UserAdminAdd'))
app.add_url_rule('/admin/user/login', view_func=UserAdminLogin.as_view('UserAdminLogin'))
app.add_url_rule('/admin/user/logout', view_func=UserAdminLogout.as_view('UserAdminLogout'))

# Client
app.add_url_rule('/user/login', view_func=UserLogin.as_view('UserLogin'))
app.add_url_rule('/user/register', view_func=UserRegister.as_view('UserRegister'))
app.add_url_rule('/user/logout', view_func=UserLogout.as_view('UserLogout'))

@app.errorhandler(404)
def err_404(err):
    return redirect('/')