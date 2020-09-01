from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Blog.config import Database
from flask_migrate import Migrate

# Intialize app instance
app = Flask(__name__, template_folder='templates')
app.secret_key = 'abcdef123434#$#$abc8738473'

# Set database connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    Database.USER,
    Database.PWD,
    Database.HOST,
    Database.PORT,
    Database.DB
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Initialize sqlalchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def run_migration():
    from Blog.src.User.Model import User
    from Blog.src.Post.Model import Post
    from Blog.src.Comment.Model import Comment

    return