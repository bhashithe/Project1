from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
import psycopg2 as dbl
import psycopg2.extras
import sys
import datetime
import json
from flask_wtf import Form
from wtforms import StringField, PasswordField, TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError

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
            email = username

            # Compare Passwords
            if (password_candidate == password):
                # Passed
                session['logged_in'] = True
                session['username'] = fname
                session['email'] = email

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

class ProfileForm(Form):
   fname = TextField("First Name",[validators.Required("Please enter a first name.")])
   lname = TextField("Last Name",[validators.Required("Please enter a last name.")])
   Address1 = TextField("Address1",[validators.Required("Please enter a street")])
   Address2 = TextField("Address2")
   city = TextField("City",[validators.Required("Please enter a city")])
   state = SelectField('State', choices = [('GA', 'GA'), 
      ('TX', 'TX')])
   zipcode = IntegerField("Zipcode",[validators.Required("Please enter a valid zipcode")])
   GREQ = IntegerField("GREQ")
   GREV = IntegerField("GREV")
   GREA = IntegerField("GREA")
   TOEFL = IntegerField("TOEFL")
   
   submit = SubmitField("Send")
    

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    form = ProfileForm()
    email = session['email']
    conn = dbl.connect(database='graddb', user='Cynthia', password='123')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('profile.html', form = form)
        else:
            fname = form.fname.data
            lname = form.lname.data
            Address1 = form.Address1.data
            Address2 = form.Address2.data
            city = form.city.data
            state = form.state.data
            zipcode = form.zipcode.data
            GREQ = form.GREQ.data
            GREV = form.GREV.data
            GREA = form.GREA.data
            TOEFL = form.TOEFL.data
            
            postgreSQL_select_Query = "UPDATE applicant SET fname=%s,lname=%s, address1=%s, address2=%s, city=%s, state=%s, zip=%s, greq=%s, grev=%s, grea=%s, toefl=%s where email=%s;"
            cursor.execute(postgreSQL_select_Query, (fname, lname, Address1, Address2, city, state, zipcode, GREQ, GREV, GREA, TOEFL, email))
            conn.commit()
            print('Profile updated')
    return render_template('profile.html', form = form)

class ApplicationForm(Form):
   university = SelectField('Department',choices = [('GSU', 'GSU'), 
      ('GSU', 'GSU')])
   dname = SelectField('Department',choices = [('CSC', 'Computer Science'), 
      ('PHYS', 'Physics')])
   program = SelectField('Program',choices = [('MS', 'Masters'), 
      ('PhD', 'PhD')])
   term = SelectField('Term Of Admission', choices = [('FA', 'Fall'), 
      ('SP', 'Spring'), ('SU', 'Summer')])
   year = SelectField('Year Of Admission', choices = [('2019', '2019'), 
      ('2020', '2020')])
    
   submit = SubmitField("Send")

@app.route('/application', methods=['GET', 'POST'])
def application():
    form = ApplicationForm()
    email = session['email']
    conn = dbl.connect(database='graddb', user='Cynthia', password='123')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    postgreSQL_select_Query = "SELECT admissionStatus FROM application where email=%s;"
    cursor.execute(postgreSQL_select_Query, (email,))
    data = cursor.fetchone()
    
    if request.method == 'POST':
        university = form.university.data
        dname = form.dname.data
        program = form.program.data
        term = form.term.data
        year = form.year.data
        date = datetime.datetime.today()
        
        postgreSQL_select_Query = "SELECT email FROM application where email=%s;"
        cursor.execute(postgreSQL_select_Query, (email,))
        #if user exists
        if cursor.rowcount > 0:
            postgreSQL_select_Query = "UPDATE application SET university=%s,dname=%s, program=%s, termOfAdmission=%s, yearOfAdmission=%s, where email=%s;"
            cursor.execute(postgreSQL_select_Query, (university, dname, program, term, year, email))
            conn.commit()
        else:
            postgreSQL_select_Query = "INSERT INTO application (email,university,dname, program, dateOfApp,termOfAdmission, yearOfAdmission, admissionStatus) VALUES (%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(postgreSQL_select_Query, (email, university, dname, program, date, term, year, 'PENDING'))
            conn.commit()
        return render_template('home.html')
    else:
        #if admissionStatus is not null
        if data is None:
            return render_template('application.html', form=form)
        else:
            session['status'] = data['admissionstatus']
            flash('Your application is  ' + session['status'])
            return render_template('home.html')
            
@app.route('/director', methods=['GET','POST'])
def director():
    conn = dbl.connect(database='graddb', user='Cynthia', password='123')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT email FROM application WHERE admissionStatus = \'PENDING\';")
    data = cursor.fetchall()
    
    return render_template('director.html', data=data)

@app.route('/decision/<item>', methods=['GET','POST'])
def decision(item):
    conn = dbl.connect(database='graddb', user='Cynthia', password='123')
    cursor = conn.cursor()
    if item == "ACCEPT" or item == "REJECT":
        postgreSQL_select_Query = "UPDATE application SET admissionStatus=%s where email=%s;"
        cursor.execute(postgreSQL_select_Query, (item, session['applicantemail']))
        conn.commit()
        session.clear()
        return redirect(url_for('director'))
    else:
        session['applicantemail'] = item
        cursor.execute("SELECT a.fname, a.lname, a.greq, a.grev, a.grea, a.toefl, b.program, b.termofadmission FROM applicant a inner join application b on a.email = b.email WHERE a.email = %s;", (item,))
        data = cursor.fetchall()
        return render_template('decision.html', data=data)

def sentToPAWS():
    connection = dbl.connect(database='graddb', user='Cynthia', password='123')
    cursor = connection.cursor()
    postgreSQL_select_Query = "UPDATE application SET dataSentToPaws = \'Yes\' WHERE admissionStatus = \'ACCEPT\';"
    cursor.execute(postgreSQL_select_Query)
    connection.commit()


#Send data to Paws
@app.route('/acceptedStudents/<string:uni>', methods=['GET'])
def acceptedStudents(uni) :
    conn = dbl.connect(database='graddb', user='Cynthia', password='123')
    cursor = conn.cursor()
    cursor.execute("UPDATE application SET datasenttopaws = \'No\' WHERE datasenttopaws IS NULL;")
    conn.commit()
    cur = conn.cursor()
    cur.execute('SELECT a.fname, a.lname, a.email FROM applicant a INNER JOIN application b ON a.email = b.email WHERE b.university=%s AND b.admissionStatus=\'ACCEPT\' AND dataSentToPaws <> \'Yes\';',(uni,))
    columns = ['fname','lname','email']
    answers = []
    rows = cur.fetchall()
    for row in rows:
        answers.append(dict(zip(columns,row)))
    conn.close()
    result = {"students":answers}
    sentToPAWS()
    return json.dumps(result, indent=2)

#Given university, term, and year, return university level statistics of applicants 
#(for each department and program, return number of applicants, number of accepts, number of rejects, and number of pending decisions).
@app.route('/universityStats/<string:uni>/<string:term>/<int:year>', methods=['GET'])
def universityStats(uni, term, year) :
    conn = dbl.connect(database='graddb', user='Cynthia', password='123')
    cur = conn.cursor()
    postgreSQL_select_Query = "SELECT Y.dname, Y.program, Y.accepted, Y.rejected, Y.pending, (Y.accepted + Y.rejected + Y.pending) AS total FROM(select X.dname, X.program, MAX(CASE WHEN X.admissionstatus = 'ACCEPT' THEN X.applicants ELSE 0 END) AS Accepted, MAX(CASE WHEN X.admissionstatus = 'REJECT' THEN X.applicants ELSE 0 END) AS Rejected, MAX(CASE WHEN X.admissionstatus = 'PENDING' THEN X.applicants ELSE 0 END) AS Pending FROM (select dname, program, count(email) as applicants, admissionStatus FROM application WHERE university = %s AND termOfAdmission = %s AND yearOfAdmission = %s GROUP BY dname, program, admissionStatus ) X GROUP BY X.dname, X.program) Y;"
    cur.execute(postgreSQL_select_Query,(uni,term,year))
    columns = ['dname','program','accepted','rejected','pending','total']
    answers = []
    rows = cur.fetchall()
    for row in rows:
        answers.append(dict(zip(columns,row)))
    conn.close()
    result = {uni + " students":answers}
    return json.dumps(result, indent=2)

#Given university, department, term, and year, return department level statistics of applicants 
#(for each program, return number of applicants, number of accepts, number of rejects, and number of pending decisions).
@app.route('/departmentStats/<string:uni>/<string:dept>/<string:term>/<int:year>', methods=['GET'])
def departmenyStats(uni, dept, term, year) :
    conn = dbl.connect(database='graddb', user='Cynthia', password='123')
    cur = conn.cursor()
    postgreSQL_select_Query = "SELECT Y.program, Y.accepted, Y.rejected, Y.pending, (Y.accepted + Y.rejected + Y.pending) AS total FROM(SELECT X.program,MAX(CASE WHEN X.admissionstatus = 'ACCEPT' THEN X.applicants ELSE 0 END) AS Accepted, MAX(CASE WHEN X.admissionstatus = 'REJECT' THEN X.applicants ELSE 0 END) AS Rejected,MAX(CASE WHEN X.admissionstatus = 'PENDING' THEN X.applicants ELSE 0 END) AS Pending FROM (select program, count(email) as applicants, admissionStatus from application WHERE university = %s AND dname = %s AND termofadmission = %s AND yearOfAdmission = %s GROUP BY program, admissionStatus ) X GROUP BY X.program) Y"
    cur.execute(postgreSQL_select_Query,(uni,dept,term,year))
    columns = ['program','accepted','rejected','pending','total']
    answers = []
    rows = cur.fetchall()
    for row in rows:
        answers.append(dict(zip(columns,row)))
    conn.close()
    result = {dept + " students":answers}
    return json.dumps(result, indent=2)


if __name__ == '__main__':
     app.secret_key='secret123'
     app.run(debug=True)

