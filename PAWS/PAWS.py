from flask import Flask, request, render_template, session, redirect, Session
from flask.json import jsonify
from lib.Database import Database
from lib.Student import Student
from lib.Admin import Admin
from lib.Department import Department

import requests
import json

app = Flask(__name__)
sess = Session()

@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return redirect('/home/')
    else:
        return redirect('/login/')

@app.route('/home/')
def home():
    if not session.get('logged_in'):
        return redirect('/login/')
    else:
        if request.method == 'GET':
            return render_template('home.html', login=session['logged_in'], user=Student(session['id']))

@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'POST' and request.form:
        password = request.form['password']
        sid = request.form['sid']
        s = Student(sid)
        if s.register(password):
            return redirect('/login/')
        else:
            return "registration error"
    elif request.method == 'GET':
        return render_template('register.html', title='register', login=session['logged_in'])

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', login=session['logged_in'])
    elif request.method == 'POST':
        s = Student(request.form['sid'])
        if s.login(request.form['password']):
            session['logged_in'] = True
            session['id'] = request.form['sid']
            return redirect('/home/')
        else:
            session['logged_in'] = False
            return "wrong"
    else:
        return "someshit went wront"

@app.route('/logout/', methods=['GET'])
def logout():
   session['logged_in'] = False
   session['id'] = False
   return redirect('/login/')

@app.route('/dummy', methods=['GET'])
def dummy_data():
    data = [{"sid":1009, "email":"varshi@gmail.com", "fname":"Varshi", "lname":"Abeysinghe", "majordept":"CSC", "gradassistant":"Y"}]
    return jsonify(data)

@app.route('/request/', methods=['GET'])
def request_accepted():
    data = json.loads(requests.get('http://localhost:5013/dummy').content)
    Admin.accepted_req(data)
    return 'student added'

@app.route('/students/<string:dept>/', methods=['GET'])
def students_dept(dept):
    return jsonify(Student.student_list(dept))

@app.route('/courses/<string:dept>/', methods=['GET'])
def course_dept(dept):
    return jsonify(Department.getcourses(dept))

@app.route('/students/enrolled/<string:dept>/<string:term>/', methods=['GET'])
def enrollment(dept, term):
    return jsonify(Student.enrollment_list(dept, term))

@app.route('/Admin/student/<int:sid>/grade/<int:crn>/', methods=['POST'])
def update_grade(sid, crn):
    if request.json:
        Admin.update_grade(sid, request.json['term'], request.json['year'], crn, request.json['grade'])
        return "update successfull"

if __name__ =='__main__':
    app.secret_key = 'super secret key here gghalfndfacvdaewa'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='tinman.cs.gsu.edu', debug=True, port=5013)
