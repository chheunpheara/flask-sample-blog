from Blog.app import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(128))
    status = db.Column(TINYINT(), default=1)
    post = relationship('Post')
    comment = relationship('Comment')