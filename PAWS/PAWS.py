from flask import Flask, request
from lib.Database import Database
from lib.Student import Student
from lib.Admin import Admin

app = Flask(__name__)

@app.route('/register/', methods=['POST'])
def register():
	if request.method == 'POST' and request.json:
		password = request.json['password']
		sid = request.json['sid']
		s = Student(sid)
		s.register(password)
	return 'student registered successfully '+ str(s.getdata())

@app.route('/request/', methods=['POST'])
def request_accepted():
	if request.method == 'POST' and request.json:
		Admin.accepted_req(request.json)
		return 'student added'

@app.route('/students/<string:dept>/', methods=['GET'])
def students(dept):
	return str(Student.student_list(dept))

@app.route('/view')
def view():
	s = Student(1000)
	d = s.getdata()
	return '<p>'+str(d)+'</p>'

if __name__ =='__main__':
    app.run(debug=True, port=5013)
