from flask import Flask
from lib import Database

app = Flask(__name__)

@app.route('/home')
def home():
    return '<h1>hello world</h1>'

@app.route('/register', method=['POST'])
def register():
    return '<h1>register</h1>'

if __name__ =='__main__':
    app.run(debug=True)
