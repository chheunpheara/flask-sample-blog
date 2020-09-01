from Blog.app import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import datetime

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.Text(), nullable=False)
    reply_to_comment = db.Column(db.Text())
    reply_to_comment_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer, ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    reply_to_comment_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)