from flask import Flask, render_template, request, redirect, url_for, session, json,jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from sqlalchemy import update
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
        .query(Application_receipt,Complect,Brand,Model,Fason,Category)\
        .filter(Application_receipt.provider_id == curent_id)\
        .join(Complect)\
        .filter(Application_receipt.complect_id == Complect.id)\
        .join(Brand)\
        .filter(Complect.brands_id == Brand.id)\
        .join(Model)\
        .filter(Complect.models_id == Model.id)\
        .join(Fason)\
        .filter(Complect.fason_id == Fason.id) \
        .join(Category) \
        .filter(Fason.categories_id == Category.id)


    conn.close()

    return render_template('mainPage.html',curent_user=sesion_user_login
                        ,second_table = join_table
                           )




@app.route('/receipt',methods=['GET','POST'])
def receipt_application():
    form = ReceiptForm(request.form)
    conn = db.engine.connect()
    session_user_login = session['curent_user']

    categories_names = db.session.query(Category)
    fason_names = db.session.query(Fason)

    if request.method == 'POST' and form.validate():

        id_category = request.form['categor']
        category_price = Category.query.filter_by(id=id_category).first().price
        name_fason = request.form['fas']


        brand_name = form.brand.data
        model_name = form.model.data
        if db.session.query(Brand.name).filter_by(name=brand_name).scalar() == None:
            brand_app = Brand(brand_name)
            db.session.add(brand_app)
        if db.session.query(Model.name).filter_by(name=model_name).scalar() == None:
            model_app = Model(model_name)
            db.session.add(model_app)
        db.session.commit()

        complect_fason_id = db.session.query(Fason.id).filter_by(name = name_fason)
        complect_brand_id = db.session.query(Brand.id).filter_by(name = brand_name)
        complect_model_id = db.session.query(Model.id).filter_by(name = model_name)

        complect_app = Complect(complect_fason_id, complect_brand_id, complect_model_id)
        db.session.add(complect_app)
        db.session.commit()

        app_complect_id = conn.execute('select id from complect order by id desc limit 1')
        app_complect_id = app_complect_id.fetchone()
        app_complect_id = app_complect_id[0]
        app_quantity = form.quantity.data
        app_date_adoption = form.date_adoption.data
        app_date_issue = form.date_issue.data
        app_provider_id = User.query.filter_by(login=session_user_login).first().id
        app_price = app_quantity * category_price
        app_confirmed = False

        #date_adoption = now().format('YYYY-MM-DD')
        receipt_app = Application_receipt(app_complect_id,app_quantity,app_date_adoption,app_date_issue,app_provider_id,app_price,app_confirmed)
        db.session.add(receipt_app)
        db.session.commit()
        conn.close()

        return redirect(url_for('main_page'))

    return render_template('applicationForReceipt.html', form = form, categoty_html = categories_names,fason_html=fason_names)


@app.route('/admin', methods=['GET','POST'])
def AdminPage():
    conn = db.engine.connect()
    join_table_admin = db.session \
        .query(Application_receipt, Complect, Brand, Model, Fason, Category, User) \
        .join(Complect) \
        .filter(Application_receipt.complect_id == Complect.id) \
        .join(Brand) \
        .filter(Complect.brands_id == Brand.id) \
        .join(Model) \
        .filter(Complect.models_id == Model.id) \
        .join(Fason) \
        .filter(Complect.fason_id == Fason.id) \
        .join(Category) \
        .filter(Fason.categories_id == Category.id)\
        .join(User)\
        .filter(Application_receipt.provider_id == User.id)

    conn.close()

    if request.method == 'POST':
        conn = db.engine.connect()
        app_id = request.form['but1']
        app_id = app_id[7:]
        #confirmed_button = Application_receipt(confirmed=True)
        #print(confirmed_button)
        db.session.query(Application_receipt).filter(Application_receipt.id == app_id).\
            update({'confirmed':True})
        db.session.commit()
        conn.close()

        return redirect(url_for('AdminPage'))

    return render_template('adminPage.html',admin_table = join_table_admin)

@app.route('/handler1',methods=['POST'])
def AjaxCategory():
    id_category = request.form['categor']
    return json.dumps({'status': 'OK','brand': id_category})


# @app.route('/handler2',methods=['POST'])
# def AjaxAdmin():
#     id_app = request.form['app_id']
#     print(id_app)
#     return json.dumps({'status': 'OK','brand': id_app})

# @app.route('/user/<nickname>')
# def user(nickname):
#     user = User.query.filter_by(nickname = nickname).first()
#
#     return render_template('user.html')

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
