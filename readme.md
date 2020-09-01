### Blog - Flask Tutorial
A sample blog application to learn Flask + SqlAlchemy


### Installation
    pip install -r requirements.txt

### Run Migration
Change directory to `Blog` and run:
    
    flask db init

    flask db migrate -m 'Your commit message'

    flask db upgrade


Read more about Flask-Migrate at; https://flask-migrate.readthedocs.io/en/latest/

### Run the application
Make sure you are still at `Blog`

    export FLASK_APP=app
    export FLASK_ENV=development
    flask run


