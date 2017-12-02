from wtforms import Form,StringField,TextAreaField,PasswordField,validators,\
    BooleanField, IntegerField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from warehouseDB_ORM import Category, Fason

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


class LoginForm(Form):
    login = StringField('Login', [validators.Length(min=5, max=50)])
    password = PasswordField('Password', [validators.DataRequired()])
    #remember = BooleanField('remember me')


class RegisterForm(Form):
    login = StringField('Login', [validators.Length(min=5, max=50)])
    password = StringField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')
    email = StringField('Email', [validators.Length(min=6,max=50)])
    username = StringField('Username',[validators.Length(min=4, max=25)])


class ReceiptForm(Form):
    brand = StringField('Brand',[validators.Length(min=2, max=50)])
    model = StringField('Model',[validators.Length(min=2, max=50)])
    quantity = IntegerField('Quantity')
    date_adoption = DateField('Data adoption')
    date_issue = DateField('Data isuue')
