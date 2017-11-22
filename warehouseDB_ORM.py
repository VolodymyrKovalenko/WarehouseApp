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
    category = db.Column(db.String(45))
    fason = db.Column(db.String(45))
    brand = db.Column(db.String(45))
    model = db.Column(db.String(45))
    applications_receipt = db.relationship('Application_receipt', backref='applic', lazy='dynamic')

    def __init__(self,category,fason,brand,model):
        self.category = category
        self.fason = fason
        self.brand = brand
        self.model = model

class Application_receipt(db.Model):
    __tablename__ = 'application_receipt'
    id = db.Column(db.INTEGER, primary_key=True)
    complect_id = db.Column(db.INTEGER, db.ForeignKey('complect.id'))
    quantity = db.Column(db.INTEGER)
    date_adoption = db.Column(db.Date)
    date_issue = db.Column(db.Date)
    provider_id = db.Column(db.INTEGER)

    def __init__(self,complect_id, quantity,date_adoption,date_issue, provider_id):
        self.complect_id = complect_id
        self.quantity = quantity
        self.date_adoption = date_adoption
        self.date_issue = date_issue
        self.provider_id = provider_id

class Sklad(db.Model):
    __tablename__ = 'sklad'
    id = db.Column(db.INTEGER, primary_key = True)
    application_id = db.Column(db.INTEGER)
    price = db.Column(db.INTEGER)

if __name__ == '__main__':
    manager.run()


#db.create_all()






#admin = User('Ostap39','i44easy99lab61','admin10@example.com','dydyaStosa7')
#db.create_all() # In case user table doesn't exists already. Else remove it.
#db.session.add(admin)
#db.session.commit() # This is needed to write the changes to database
#User.query.all()
#User.query.filter_by(username='admin').first()