from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:234344@localhost:3306/new1_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Example(db.Model):
    __tablename__ = 'example'
    id = db.Column('id', db.INTEGER, primary_key=True)
    data = db.Column('data', db.Unicode)

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
