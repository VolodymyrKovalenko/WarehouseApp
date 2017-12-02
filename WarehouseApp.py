from flask import Flask, render_template, request, redirect, url_for, session, json,jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from sqlalchemy.orm import query
from sqlalchemy.sql import select
import time


from forms import LoginForm, RegisterForm, ReceiptForm
from warehouseDB_ORM import User,Application_receipt, Complect, Category, Fason, Brand, Model
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

    sesion_user_login = session['curent_user']# counterpart for session
    curent_id = User.query.filter(User.login == sesion_user_login).first()
    curent_id = curent_id.id

    join_table = db.session\
        .query(Application_receipt, Complect)\
        .join(Complect)\
        .filter(Application_receipt.provider_id == curent_id)

    conn.close()

    return render_template('mainPage.html',curent_user=sesion_user_login,first_table_result =  join_table)




@app.route('/receipt',methods=['GET','POST'])
def receipt_application():
    print('work_receipt')
    form = ReceiptForm(request.form)
    conn = db.engine.connect()
    session_user_login = session['curent_user']

    categories_names = db.session.query(Category)

    fason_names = db.session.query(Fason)



    if request.method == 'POST' and form.validate():

        category_name = form.category_opt.data
        category_price = form.price.data

        fason_name = form.fason_opt.data
        fason_category_id = None

        complect_category_id = None
        complect_brand_id = None
        complect_model_id = None

        brand_name = form.brand.data
        model_name = form.model.data

        app_quantity = form.quantity.data
        app_date_adoption = form.date_adoption.data
        app_date_issue = form.date_issue.data
        app_confirmed = False
        app_provider_id = User.query.filter_by(login=session_user_login).first().id

        #date_adoption = now().format('YYYY-MM-DD')

        #category_receipt_app = Category(category_name,category_price)
        #fason_app = Fason(fason_name,fason_category_id)
        complect_app = Complect(complect_category_id,complect_brand_id,complect_model_id)
        brand_app = Brand(brand_name)
        model_app = Model(model_name)

        #db.session.add(category_receipt_app)
        #db.session.add(fason_app)
        db.session.add(complect_app)
        db.session.add(brand_app,model_app)
        db.session.commit()


        complect_id = conn.execute('select id from complect order by id desc limit 1')
        complect_id = complect_id.fetchone()
        complect_id = complect_id[0]


        receipt_app = Application_receipt(complect_id,app_quantity,app_date_adoption,app_date_issue,app_provider_id,app_confirmed)
        db.session.add(receipt_app)
        db.session.commit()
        conn.close()

        return redirect(url_for('main_page'))

    return render_template('applicationForReceipt.html', form = form, categoty_html = categories_names,fason_html=fason_names)

@app.route('/handler1',methods=['POST'])
def AjaxCategory():
    category = request.form['categor']
    session['curent_category'] = category
    print('my category is:',category)
    return json.dumps({'status': 'OK','brand': category})






# @app.route('/Test1')
# def signUp():
#     return render_template('Test1.html'), jsonify({'key':'it work'})
#
# @app.route('/AloUser', methods=['POST'])
# def Obrabotka():
#     print('work1')
#     user =  request.form['username']
#     password = request.form['password']
#     print(user)
#     return json.dumps({'status':'OK','user':user,'pass':password})



if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
