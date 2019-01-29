from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
import psycopg2 as dbl
import psycopg2.extras
import sys
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# get a connection, if a connect cannot be made an exception will be raised here
conn = dbl.connect(database='graddb', user='Cynthia', password='123')
 
# conn.cursor will return a cursor object, you can use this cursor to perform queries
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

class RegisterForm(Form):
    fname = StringField('First Name', [validators.length(min=1, max=50)])
    lname = StringField('Last Name', [validators.length(min=1, max=50)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password = form.password.data

        cursor.execute("INSERT INTO applicant(fname, lname, email, password) VALUES(%s, %s, %s, %s)", (fname, lname, email, password))

        flash('You are now registered and can log in', 'success')

        return 'Registered'

    return render_template('register.html', form=form)

if __name__ == '__main__':
     app.secret_key='secret123'
     app.run(debug=True)

