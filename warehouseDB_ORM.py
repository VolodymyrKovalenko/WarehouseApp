#!/usr/bin/env python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask import Flask, render_template, request, redirect, url_for, session, json

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import click

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(80), unique=True)
    applications_user = db.relationship('Application_receipt', backref='applic_user', lazy='dynamic')

    def __init__(self, login, password, email, username):
        self.login = login
        self.password = password
        self.email = email
        self.username = username


    def __repr__(self):
        return '<User %r>' % self.username

class Complect(db.Model):
    __tablename__ = 'complect'
    id = db.Column(db.INTEGER, primary_key=True)
    applications_receipt = db.relationship('Application_receipt', backref='applic', lazy='dynamic')
    fason_id = db.Column(db.INTEGER, db.ForeignKey('fason.id'))
    brands_id = db.Column(db.INTEGER,db.ForeignKey('brand.id'))
    models_id = db.Column(db.INTEGER, db.ForeignKey('model.id'))

    def __init__(self,fason_id,brands_id,models_id):
        self.fason_id = fason_id
        self.brands_id = brands_id
        self.models_id = models_id

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45), unique=True)
    price = db.Column(db.INTEGER)
    fasons = db.relationship('Fason', backref='fason', lazy='dynamic')


    def __init__(self,name,price):
        self.name = name
        self.price = price

class Fason(db.Model):
    __tablename__= 'fason'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45))
    categories_id = db.Column(db.INTEGER, db.ForeignKey('category.id'))
    complects = db.relationship('Complect', backref='complect1', lazy='dynamic')

    def __init__(self,name,category_id):
        self.name = name
        self.category_id = category_id

class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45))
    complects = db.relationship('Complect', backref='complect2', lazy='dynamic')

    def __init__(self,name):
        self.name = name

class Model(db.Model):
    __tablename__ = 'model'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45))
    complects = db.relationship('Complect', backref='complect3', lazy='dynamic')

    def __init__(self,name):
        self.name = name


class Application_receipt(db.Model):
    __tablename__ = 'application_receipt'
    id = db.Column(db.INTEGER, primary_key=True)
    complect_id = db.Column(db.INTEGER, db.ForeignKey('complect.id'))
    quantity = db.Column(db.INTEGER)
    date_adoption = db.Column(db.Date)
    date_issue = db.Column(db.Date)
    provider_id = db.Column(db.INTEGER,db.ForeignKey('user.id'))
    price = db.Column(db.INTEGER)
    confirmed = db.Column(db.BOOLEAN)

    def __init__(self,complect_id, quantity,date_adoption,date_issue, provider_id,price,confirmed):
        self.complect_id = complect_id
        self.quantity = quantity
        self.date_adoption = date_adoption
        self.date_issue = date_issue
        self.provider_id = provider_id
        self.price = price
        self.confirmed = confirmed

class Sklad(db.Model):
    __tablename__ = 'sklad'
    id = db.Column(db.INTEGER, primary_key = True)
    application_id = db.Column(db.INTEGER)
    amount_days = db.Column(db.INTEGER)
    overall_price = db.Column(db.INTEGER)
    issued = db.Column(db.BOOLEAN, default=False)

if __name__ == '__main__':
    manager.run()


#db.create_all()






#admin = User('Ostap39','i44easy99lab61','admin10@example.com','dydyaStosa7')
#db.create_all() # In case user table doesn't exists already. Else remove it.
#db.session.add(admin)
#db.session.commit() # This is needed to write the changes to database
#User.query.all()
#User.query.filter_by(username='admin').first()