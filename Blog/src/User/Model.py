from Blog.app import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    status = db.Column(TINYINT(), server_default=str(1))
    post = relationship('Post')


class FrontUser(db.Model):
    __tablename__ = 'post_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    status = db.Column(TINYINT(), server_default=str(1))
    comment = relationship('Comment')
    created_at = db.Column(db.DateTime)