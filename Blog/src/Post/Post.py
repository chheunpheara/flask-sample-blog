from flask.views import View
from flask import render_template
from flask import request, redirect, flash, url_for
from .Model import Post as PostModel, db
from Blog.src.User.User import is_authenticated, get_user_id
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
    @is_authenticated
    def dispatch_request(self):
        posts = db.session.query(PostModel).all()
        return render_template('admin/post/index.html', title='Posts', posts=posts)

class PostAdminAdd(View):
    
    methods = ['GET', 'POST']

    @is_authenticated
    def dispatch_request(self):
        if request.method == 'POST':
            title = request.form['title']
            descr = request.form['descr']
            short_descr = request.form['short_descr']

            if not title:
                flash('Please enter title', 'error')
                return redirect(url_for(request.endpoint))

            if not short_descr:
                flash('Please enter short description', 'error')
                return redirect(url_for(request.endpoint))

            # Create post
            try:
                if get_user_id() == 0:
                    flash('Unable to create post', 'error')
                    return redirect(url_for(request.endpoint))

                db.session.add(
                    PostModel(
                        title=title,
                        description=descr,
                        short_description=short_descr,
                        status=1,
                        user_id=get_user_id(),
                        created_at=datetime.datetime.now()
                    )
                )

                db.session.commit()
                flash('Post created', 'success')
                return redirect(url_for('PostAdmin'))
            except (Exception) as e:
                flash(str(e), 'error')
                return redirect(url_for(request.endpoint))
            
        return render_template('admin/post/form.html', title='Post', submit_tag='Create')