from flask import Flask, request
from flask.json import jsonify
from lib.Database import Database
from lib.Student import Student
from lib.Admin import Admin
from lib.Department import Department

import requests
import json

app = Flask(__name__)

@app.route('/register/', methods=['POST'])
def register():
	if request.method == 'POST' and request.json:
		password = request.json['password']
		sid = request.json['sid']
		s = Student(sid)
		s.register(password)
	return 'student registered successfully '+ str(s.getdata())

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
    app.run(debug=True, port=5013)
