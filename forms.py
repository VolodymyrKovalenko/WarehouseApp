from wtforms import Form,StringField,TextAreaField,PasswordField,validators, BooleanField

class LoginForm(Form):
    login = StringField('Login', [validators.Length(min=5, max=50)])
    password = PasswordField('Password', [validators.DataRequired()])
    #remember = BooleanField('remember me')


class RegisterForm(Form):
    login = StringField('Login', [validators.Length(min=5, max=50)])
    password = StringField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')
    email = StringField('Email', [validators.Length(min=6,max=50)])
    username = StringField('Username',[validators.Length(min=4, max=25)])