from flask import Flask,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from os import path
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

csrf = CSRFProtect()
db=SQLAlchemy()
DB_NAME= "applicantrecords.db"

engine = create_engine(f'sqlite:///{DB_NAME}')
Session = sessionmaker(bind=engine)


def create_app():
    app = Flask(__name__)
    csrf.init_app(app)
    app.config['SECRET_KEY'] = '1@7lj@!g_ytr#$_l)x8#-6akhf6wg74_0ho!e94a#2u$r^=jo'
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .queries.insert import insert_bp
    from .queries.update import update_bp
    from .queries.delete import delete_bp
    from .queries.diagnostic_dashboard import diagnostic_dashboard
    from .queries.handson_dashboard import handson_dashboard
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(insert_bp, url_prefix='/')
    app.register_blueprint(update_bp,url_prefix='/')
    app.register_blueprint(delete_bp,url_prefix='/')
    app.register_blueprint(diagnostic_dashboard,url_prefix ='/')
    app.register_blueprint(handson_dashboard,url_prefix ='/')
    from .models import Admin, DiagnosticResults, HandsonResults, HistoryTable
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.filter_by(admin_id=int(user_id)).first()
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created the Database!")
