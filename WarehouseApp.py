from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


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

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45), unique=True)
    material = relationship("Material", back_populates="category")

class Material(db.Model):
    __tablename__ = 'material'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45), unique=True)
    category_id = db.Column(db.INTEGER, db.ForeignKey('category.id'))
    category = relationship("Category", back_populates="material")

admin = User('Ostap16','i44easy99labs57','admin3@example.com','dydyaStopa3')

db.create_all() # In case user table doesn't exists already. Else remove it.

db.session.add(admin)

db.session.commit() # This is needed to write the changes to database

User.query.all()

User.query.filter_by(username='admin').first()




@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/SignUp')
def registrarion():
    return render_template('registration.html')

@app.route('/LogIn')
def login():
    return render_template('singIn.html')

@app.route('/main')
def main_page():
    return render_template('mainPage.html')


if __name__ == '__main__':
    app.run()
