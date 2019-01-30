from wtforms import Form, StringField, TextAreaField, PasswordField, validators

class RegisterForm():

    def __init__(self, Form):
        """Return a Customer object whose name is *name*.""" 
        self.Form = Form
        self.fname = StringField('First Name', [validators.length(min=1, max=50)])
        self.lname = StringField('Last Name', [validators.length(min=1, max=50)])
        self.email = StringField('Email', [validators.length(min=6, max=50)])
        self.password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
        self.confirm = PasswordField('Confirm Password')