from flask.views import View
from flask import render_template
from flask import request, redirect, flash, url_for, session
from .Model import Post as PostModel, db
from Blog.src.Comment.Model import Comment
from Blog.src.User.Model import FrontUser
from Blog.src.User.User import is_authenticated, get_user_id, is_authenticated_client
import datetime
import sys

class Post(View):
    # def __init__(self, template):
    #     self.template = template

    # def dispatch_request(self):
    #     return render_template(self.template, title='Latest Posts')

    def dispatch_request(self):
        posts = db.session.query(PostModel).order_by(PostModel.id.desc()).all()
        return render_template('post/index.html', title='Latest Posts', posts=posts)


class PostView(View):

    methods = ['GET', 'POST']

    def dispatch_request(self, id: int):
        if request.method == 'POST':
            comment = request.form['comment']
            comment = comment.strip()
            if not comment:
                return redirect(url_for(request.endpoint, id=id))
            try:
                if 'login' not in session:
                    return redirect(url_for('UserLogin'))

                db.session.add(
                    Comment(
                        comment=comment,
                        post_id=id,
                        user_id=session['login']['id'],
                        created_at=datetime.datetime.now()
                    )
                )
                db.session.commit()
            except (Exception) as e:
                flash(str(e), 'error')

            return redirect(url_for(request.endpoint, id=id))

        post = db.session.query(PostModel).filter(PostModel.id==id).first()

        comments = []
        if post:
            comments = db.session.query(Comment, FrontUser.first_name, FrontUser.last_name)\
                .join(FrontUser)\
                .filter(Comment.post_id==id)\
                .order_by(Comment.created_at.asc())\
                .all()
    
        return render_template('post/view.html', title='', post=post, comments=comments)


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