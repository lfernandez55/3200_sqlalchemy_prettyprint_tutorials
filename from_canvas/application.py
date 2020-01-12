# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

import datetime
from flask import Flask, request, render_template_string, render_template, redirect, url_for
# from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from pprint import pprint



# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///basic_app3.sqlite'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'xxxxxx@gmail.com'
    MAIL_PASSWORD = 'xxxxxx'
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'

    # Flask-User settings
    USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"


# def create_app():
""" Flask application factory """

# Create Flask app load app.config
app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')
app.config["SQLALCHEMY_ECHO"] = True
# Initialize Flask-BabelEx
# babel = Babel(app)

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    # books = db.relationship('Book', backref='category', lazy=True)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer(), primary_key=True)
    author = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category', backref='book', lazy=True)

# Create all database tables (every time a new table is added it runs this, otherwise it doesn't)
db.create_all()

# Create 'member@example.com' user with no roles
if not User.query.filter(User.email == 'member@example.com').first():
    user = User(
        email='member@example.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password=user_manager.hash_password('Password1'),
    )
    db.session.add(user)
    db.session.commit()

# Create 'admin@example.com' user with 'Admin' and 'Agent' roles
if not User.query.filter(User.email == 'luke.fernandez@gmail.com').first():
    user = User(
        email='luke.fernandez@gmail.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password=user_manager.hash_password('Password2'),
    )
    user.roles.append(Role(name='Admin'))
    user.roles.append(Role(name='Agent'))
    db.session.add(user)
    db.session.commit()






    # return app

print("what is __name__?", __name__)
# Start development web server
# if __name__ == '__main__':
#     app = create_app()
#     app.run(host='0.0.0.0', port=4000, debug=True)
#     print("does any of this run?")
