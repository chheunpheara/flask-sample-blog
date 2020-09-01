from flask.views import View
from flask import render_template
from flask import request, redirect, flash
from .Model import Post as PostModel, db
import datetime

class Post(View):
    # def __init__(self, template):
    #     self.template = template

    # def dispatch_request(self):
    #     return render_template(self.template, title='Latest Posts')

    def dispatch_request(self):
        posts = db.session.query(PostModel).order_by(PostModel.id.desc()).all()
        return render_template('post/index.html', title='Latest Posts', posts=posts)


class PostView(View):
    def dispatch_request(self, id: int):
        post = db.session.query(PostModel).filter(PostModel.id==id).first()
        return render_template('post/view.html', title='', post=post)


### Admin ###
class PostAdmin(View):
    def dispatch_request(self):
        posts = db.session.query(PostModel).all()
        return render_template('admin/post/index.html', title='Posts', posts=posts)

class PostAdminAdd(View):
    methods = ['GET', 'POST']
    def dispatch_request(self):
        if request.method == 'POST':
            title = request.form['title']
            descr = request.form['descr']
            short_descr = request.form['short_descr']

            if not title:
                flash('Please enter title', 'error')
                return redirect('/admin/post/add')

            if not short_descr:
                flash('Please enter short description', 'error')
                return redirect('/admin/post/add')

            # Create post
            try:
                db.session.add(
                    PostModel(
                        title=title,
                        description=descr,
                        short_description=short_descr,
                        status=1,
                        user_id=1,
                        created_at=datetime.datetime.now()
                    )
                )

                db.session.commit()
                flash('Post created', 'success')
                return redirect('/admin/post')
            except (Exception) as e:
                flash(str(e), 'error')
                return redirect('/admin/post/add')
            
        return render_template('admin/post/form.html', title='Post', submit_tag='Create')