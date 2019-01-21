from flask import Flask
from lib.Database import Database
from lib.Student import Student

app = Flask(__name__)

@app.route('/home')
def home():
    return '<h1>hello world</h1>'

@app.route('/register/<int:sid>/', methods=['GET'])
def register(sid):
    s = Student(sid)
    #just debuging!
    s.register('pass')
    return '<h1>register</h1>'

@app.route('/view')
def view():
    s = Student(1000)
    d = s.getdata()
    return '<p>'+str(d)+'</p>'

if __name__ =='__main__':
    app.run(debug=True)
