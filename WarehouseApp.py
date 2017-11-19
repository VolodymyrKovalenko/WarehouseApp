from flask import Flask, render_template, request, redirect, url_for, session, json
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

from forms import LoginForm, RegisterForm
from warehouseDB_ORM import User,Category,Fason,Brand,Model_number

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

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
        session['curent_user'] = admin.login

        return redirect(url_for('main_page'))
    return render_template('registration.html',form=form)


@app.route('/LogIn',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        login_form = request.form['login']
        password_form_candidate = request.form['password']
        user = User.query.filter_by(login=login_form).first()
        session['curent_user'] = user.login

        if sha256_crypt.verify(password_form_candidate,user.password):
            return redirect(url_for('main_page'))
    return render_template('singIn.html')


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/main')
def main_page():
    sesion_message = session['curent_user']  # counterpart for session
    return render_template('mainPage.html',curent_user=sesion_message)

@app.route('/receipt')
def receipt_application():
    return render_template('applicationForReceipt.html')


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
