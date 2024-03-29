from flask import Flask, request, render_template, session, redirect, Session
from flask.json import jsonify
from flask_cors import CORS
import requests
import json

#created library files
from lib.Database import Database
from lib.Student import Student
from lib.Admin import Admin
from lib.Department import Department


app = Flask(__name__)
CORS(app)
app.config['WTF_CSRF_ENABLED'] = False
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
            return render_template('home.html', login=session['logged_in'], user=Student(session['id']), depts=Department.getdepts())

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
        return render_template('login.html')
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
        return "something bad happened"

@app.route('/logout/', methods=['GET'])
def logout():
   session['logged_in'] = False
   session['id'] = False
   return redirect('/login/')

@app.route('/student/schedule/', methods=['GET'])
def schedule():
	if session.get('logged_in'):
		s = Student(session['id'])
		d = Department()
		return render_template('schedule.html', user=s, dept=d)
	else:
		return redirect('/login/')

@app.route('/student/fees/')
def fees():
	if session.get('logged_in'):
		s = Student(session.get('id'))
		return render_template('fees.html', user=s, title='Fees', userid = session.get('id'))
	else:
		return redirect('/login/')

@app.route('/student/assistantship/<int:sid>/')
def get_assistantship(sid):
	res = json.loads(requests.get(f"http://tinman.cs.gsu.edu:5020/student/assistantship/{sid}/").content)
	return jsonify(res)

@app.route('/Admin/', methods=['GET'])
def admin():
	s = Student(0)
	return render_template('admin.html', title='Admin', user=s)

@app.route('/Admin/stats/<string:term>/<int:year>/', methods=['GET'])
def stats(term, year):
	data = json.loads(requests.get(f"http://tinman.cs.gsu.edu:5015/universityStats/GSU/{term}/{year}").content)
	return jsonify(data[list(data.keys())[0]])

"""""""""""""""""""""
**** Services
"""""""""""""""""""""

@app.route('/home/data/', methods=['POST'])
def home_data():
    term, year, dept = request.json['term'], request.json['year'], request.json['dept']
    courses = Department.get_home_data(term, year, dept)
    return jsonify(courses)

@app.route('/home/add/', methods=['POST'])
def register_course():
    term, year, crn = request.json['term'], request.json['year'], request.json['crn']
    s = Student(session['id'])
    s.add_course(term, year, crn)
    return "success"

@app.route('/home/drop/', methods=['POST'])
def deregister_course():
    term, year, crn = request.json['term'], request.json['year'], request.json['crn']
    s = Student(session['id'])
    s.drop_course(term, year, crn)
    return "success"

@app.route('/students/my-courses/<int:year>/<string:term>/', methods=['GET'])
def registered_corses(year, term):
    s = Student(session['id'])
    return jsonify(s.my_courses(term, year))

@app.route('/students/courses/count/', methods=['POST'])
def count_courses():
	if request.json:
		s = Student(session.get('id'))
		count = s.count_courses(request.json['term'], request.json['year'])
		print(count)
		return jsonify(count[0])

@app.route('/students/course/', methods=['POST'])
def course_info():
	if request.json:
		crns = [int(crn) for crn in request.json]
		d = Department()
		return jsonify(d.get_course_info(crns))
	else:
		return "unsuccessfull"

@app.route('/request/', methods=['GET'])
def request_accepted():
	data = json.loads(requests.get('http://tinman.cs.gsu.edu:5015/acceptedStudents/GSU').content)
	Admin.accepted_req(data['students'])
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
    app.run(host='tinman.cs.gsu.edu', debug=True, port=5001)
