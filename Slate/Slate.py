from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
import psycopg2 as dbl
import psycopg2.extras
import sys
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

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
        try:
            connection = psycopg2.connect(user="Cynthia",
                                      password="123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="graddb")
            cursor = connection.cursor()
            postgreSQL_select_Query = "INSERT INTO applicant(email,password,fname,lname) values (%s, %s, %s, %s);"
            cursor.execute(postgreSQL_select_Query, (email, password, fname, lname))
            connection.commit()

            flash('You are now registered and can log in', 'success')

        except (Exception, psycopg2.Error) as error:
            print("Error fetching data from PostgreSQL table", error)
        finally:
            # closing database connection
            if (connection):
                cursor.close()
                connection.close()

        return redirect(url_for('register'))
    
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = dbl.connect(database='graddb', user='Cynthia', password='123')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Get user by username
        cursor.execute("SELECT email, password, fname FROM applicant WHERE email = %s;", (username,))
        
        if cursor.rowcount > 0:
            # Get stored hash
            data = cursor.fetchone()
            password = data['password']
            fname = data['fname']

            # Compare Passwords
            if (password_candidate == password):
                # Passed
                session['logged_in'] = True
                session['username'] = fname

                return redirect(url_for('home'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cursor.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return render_template('profile.html')
    return render_template('home.html')

if __name__ == '__main__':
     app.secret_key='secret123'
     app.run(debug=True)

