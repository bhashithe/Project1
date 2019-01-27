from flask import Flask
import psycopg2 as dbl

app = Flask(__name__)

@app.route('/home')
def home():
    return 'dshj'

@app.route('/login', methods=['GET'])
def login_controller():
    #connect
    conn = dbl.connect(database='graddb', user='Cynthia', password='123')
    #authenticate
    #do login
    return 'connected'

if __name__ == '__main__':
    app.run(debug=True)