from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:234344@localhost/sklad_materialov_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
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

admin = User('Ostap44','i44easy99labs55','admin@example.com','dydyaStopa')

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
