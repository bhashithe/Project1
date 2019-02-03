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

@app.route('/')
def index():
    return redirect('/home/')

@app.route('/home/')
def home():
    return 'hello world'
  
@app.route('/dummy', methods=['GET'])
def dummy_data():
  ####################### GET local data from PAWS database in ##################
    data = [{"sid":1009, "email":"varshi@gmail.com", "fname":"Varshi", "lname":"Abeysinghe", "majordept":"CSC", "gradassistant":"Y"}]
    return jsonify(data)

# @app.route('/request/<string:dept>', methods=['GET'])
# def request_accepted(dept):
#   ####################### TBD change 'dummy' to GET from PAWS database ##################
#     data = json.loads(requests.get(f"http://tinman.cs.gsu.edu:5013/students/{dept}/").content)
#     Admin.accepted_req(data)
#     return 'student added'
@app.route('/request/students', methods=['GET'])
def request_student_accepted():
  ####################### TBD change 'dummy' to GET from PAWS database ##################
    data = json.loads(requests.get(f"http://tinman.cs.gsu.edu:5013/students/CSC/").content)
    Admin.accepted_student_req(data)
    return 'sucess students'

@app.route('/request/courses', methods=['GET'])
def request_course_accepted():
  ####################### TBD change 'dummy' to GET from PAWS database ##################
    data = json.loads(requests.get(f"http://tinman.cs.gsu.edu:5013/courses/CSC/").content)
    Admin.accepted_course_req(data)
    return 'success courses'

@app.route('/request/<string:term>/', methods=['GET'])
def request_enrollment_accepted(term):
  ####################### TBD change 'dummy' to GET from PAWS database ##################
    data = json.loads(requests.get(f"tinman.cs.gsu.edu:5013/students/enrolled/CSC/{term}").content)
    Admin.accepted_req(data)
    return 'success enrollments'

@app.route('/request/grades', methods=['GET'])
def request_grade_accepted():
  ####################### TBD change 'dummy' to GET from PAWS database ##################
    data = json.loads(requests.get(f"http://tinman.cs.gsu.edu:5013/grades/CSC/").content)
    Admin.accepted_req(data)
    return 'success grade'

# @app.route('/students/<string:dept>/', methods=['GET'])
# def students_dept(dept):
#     return jsonify(Student.student_list(dept))

# @app.route('/courses/<string:dept>/', methods=['GET'])
# def course_dept(dept):
#     return jsonify(Department.getcourses(dept))

# @app.route('/students/enrolled/<string:dept>/<string:term>/', methods=['GET'])
# def enrollment(dept, term):
#     return jsonify(Student.enrollment_list(dept, term))

@app.route('/Admin/student/<int:sid>/assistantship/<int:crn>/', methods=['POST'])
def update_assistantship(sid):
    if request.json:
        Admin.update_assistantship(sid, request.json['term'], request.json['year'], crn, request.json['assistantship'])
        return "update successfull"

@app.route('/Admin/student/<int:sid>/grade/<int:crn>/', methods=['POST'])
def update_grade(sid, crn):
    if request.json:
        Admin.update_grade(sid, request.json['term'], request.json['year'], crn, request.json['grade'])
        return "update successfull"

if __name__ =='__main__':
    app.secret_key = 'super secret key here gghalfndfacvdaewa'
    app.config['SESSION_TYPE'] = 'filesystem'
    #app.run(host='tinman.cs.gsu.edu', debug=True, port=5014)
    app.run(host='localhost', debug=True)
