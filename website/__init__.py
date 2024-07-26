from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from os import path
from flask_wtf.csrf import CSRFProtect

# csrf = CSRFProtect()
db=SQLAlchemy()
DB_NAME= "applicantrecords.db"

engine = create_engine(f'sqlite:///{DB_NAME}')
Session = sessionmaker(bind=engine)


def create_app():
    app = Flask(__name__)
    # csrf.init_app(app)
    app.config['SECRET_KEY'] = '1@7lj@!g_ytr#$_l)x8#-6akhf6wg74_0ho!e94a#2u$r^=jo'
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .queries.insert import insert

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(insert, url_prefix='/')

    from .models import Admin, DiagnosticResults, HandsonResults, HistoryTable
    create_database(app)
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created the Database!")
