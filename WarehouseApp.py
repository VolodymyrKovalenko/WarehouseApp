from flask import Flask, render_template, request, redirect, url_for, session, json
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from sqlalchemy.orm import query
from sqlalchemy.sql import select


from forms import LoginForm, RegisterForm, ReceiptForm
from warehouseDB_ORM import User,Application_receipt, Complect
from arrow import now

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
            if user.login == 'admin88':
                return redirect(url_for('admin_page'))
            return redirect(url_for('main_page'))
    return render_template('singIn.html')


@app.route('/')
def start_page():
    session.clear()
    return render_template('startPage.html')

@app.route('/main',methods=['GET','POST'])
def main_page():
    conn = db.engine.connect()

    sesion_user_login = session['curent_user']  # counterpart for session

    sel_user_id = select([User.id]).where(User.login == sesion_user_login)
    user_id_result = conn.execute(sel_user_id)
    user_id_row_result = user_id_result.fetchone()

    select_app_application = select([Application_receipt]).where(Application_receipt.provider_id == user_id_row_result[0])
    select_app_complect = select([Complect]).where(Complect.id == Application_receipt.complect_id)
    products = conn.execute(select_app_application)
    conn.close()


    return render_template('mainPage.html',curent_user=sesion_user_login,allApp=products)


@app.route('/receipt',methods=['GET','POST'])
def receipt_application():
    form = ReceiptForm(request.form)
    conn = db.engine.connect()
    if request.method == 'POST' and form.validate():
        category = form.category.data
        fason = form.fason.data
        brand = form.brand.data
        model = form.model.data

        quantity = form.quantity.data
        date_adoption = form.data_adoption.data
        date_issue = form.date_issue.data

        session_user_login = session['curent_user']
        provider_id_select = select([User.id]).where(User.login == session_user_login)
        provider_id = conn.execute(provider_id_select)
        #date_adoption = now().format('YYYY-MM-DD')
        complect_receipt_app = Complect(category, fason, brand, model)
        db.session.add(complect_receipt_app)
        db.session.commit()
        complect_id_select = select([Complect.id])
        complect_id_select_res = conn.execute(complect_id_select)
        complect_id = complect_id_select_res.fetchone()

        complect_id = complect_id[-1]


        receipt_app = Application_receipt(complect_id,quantity,date_adoption,date_issue,provider_id)
        db.session.add(receipt_app)
        db.session.commit()
        conn.close()

        return redirect(url_for('main_page'))

    return render_template('applicationForReceipt.html')

#@app.route('/admin',methods=['GET','POST'])
#def admin_page():




if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
