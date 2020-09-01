from Blog.app import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(70))
    short_description = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    status = db.Column(TINYINT(), server_default=str(1))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    