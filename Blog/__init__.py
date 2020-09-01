from Blog.app import app, run_migration
from flask import render_template

# Migration status
run_migration()

# Load controllers
from Blog.src.Post.Post import *

# Initilize controllers

# Client side

# Post Controller - homepage
app.add_url_rule('/', view_func=Post.as_view('PostHome'))
app.add_url_rule('/view/<int:id>', view_func=PostView.as_view('PostView'))

# Admin side
app.add_url_rule('/admin/post', view_func=PostAdmin.as_view('PostAdmin'))
app.add_url_rule('/admin/post/add', view_func=PostAdminAdd.as_view('PostAdminAdd'))