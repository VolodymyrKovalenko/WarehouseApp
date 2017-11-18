from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from wtforms import Form,StringField,TextAreaField,PasswordField,validators, BooleanField
from passlib.hash import sha256_crypt

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
    fasons = relationship('Fason', backref='category', lazy='dynamic')

class Fason(db.Model):
    __tablename__ = 'fason'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45), unique=True)
    category_id = db.Column(db.INTEGER, db.ForeignKey('category.id'))
    brands = relationship('Brand', backref='fason', lazy='dynamic')

class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45), unique=True)
    fason_id = db.Column(db.INTEGER, db.ForeignKey('fason.id'))
    model_numbers = relationship('Model_number', backref='brand', lazy='dynamic')

class Model_number(db.Model):
    __tablename__ = 'model_number'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45),unique=True)
    brand_id = db.Column(db.INTEGER,db.ForeignKey('brand.id'))






#admin = User('Ostap39','i44easy99lab61','admin10@example.com','dydyaStosa7')
#db.create_all() # In case user table doesn't exists already. Else remove it.
#db.session.add(admin)
#db.session.commit() # This is needed to write the changes to database
#User.query.all()
#User.query.filter_by(username='admin').first()



class RegisterForm(Form):
    login = StringField('Login', [validators.Length(min=5, max=50)])
    password = StringField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')
    email = StringField('Email', [validators.Length(min=6,max=50)])
    username = StringField('Username',[validators.Length(min=4, max=25)])



@app.route('/SignUp', methods=['GET', 'POST'])
def registration():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        login = form.login.data
        password = sha256_crypt.encrypt(str(form.password.data))
        email = form.email.data
        username = form.username.data

        admin = User(login,password,email,username)
        db.session.add(admin)
        db.session.commit()

        return redirect(url_for('main_page'))
    return render_template('registration.html',form=form)

class LoginForm(Form):
    login = StringField('Login', [validators.Length(min=5, max=50)])
    password = PasswordField('Password', [validators.DataRequired()])
    #remember = BooleanField('remember me')

@app.route('/LogIn',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        login_form = request.form['login']
        password_form_candidate = request.form['password']
        user = User.query.filter_by(login=login_form).first()

        if sha256_crypt.verify(password_form_candidate,user.password):
            return redirect(url_for('main_page'))
    return render_template('singIn.html')


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/main')
def main_page():
    return render_template('mainPage.html')


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
