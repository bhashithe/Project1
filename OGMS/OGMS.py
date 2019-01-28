from flask import Flask
import psycopg2
import json

from flask_cors import CORS
from flask import request, render_template, send_from_directory

app = Flask(__name__,static_url_path='')
CORS(app)
app.config['WTF_CSRF_ENABLED'] = False

############################ TBD ####################

#app = Flask(__name__)

def shutdown_server():
  func = request.environ.get('werkzeug.server.shutdown')
  if func is None:
    raise RuntimeError('Not running with the Werkzeug Server')
  func()

def getAdvisors():
  con = psycopg2.connect(database='grad', user='raj')
  cur = con.cursor()
  cur.execute('(select distinct advisor from phd) union (select advisor from masters) order by advisor')
  columns = ['advisor']
  advisors = []
  rows = cur.fetchall()
  for row in rows:
    if row[0] != '':
      #advisors.append(dict(zip(columns,row)))
      advisors.append(row[0])
  con.close()
  result = {"advisors":advisors}
  return json.dumps(result, indent=2)

def getYears():
  con = psycopg2.connect(database='grad', user='raj')
  cur = con.cursor()
  cur.execute('(select distinct year from phd) union (select year from masters) order by year')
  columns = ['year']
  years = []
  rows = cur.fetchall()
  for row in rows:
    if row[0] != '':
      #years.append(dict(zip(columns,row)))
      years.append(row[0])
  con.close()
  result = {"years":years}
  return json.dumps(result, indent=2)

def getPhDStudentsGivenAdvisor(adv) :
  con = psycopg2.connect(database='grad', user='raj')
  cur = con.cursor()
  cur.execute('select snum, sname, advisor, coadvisor, month, year from phd where advisor=\''+adv+'\' or coadvisor=\''+adv+'\' order by year, month')
  columns = ['snum','sname','advisor','coadvisor','month','year']
  answers = []
  rows = cur.fetchall()
  for row in rows:
    answers.append(dict(zip(columns,row)))
  con.close()
  result = {"students":answers}
  return json.dumps(result, indent=2)

def getMSStudentsGivenAdvisor(adv) :
  con = psycopg2.connect(database='grad', user='raj')
  cur = con.cursor()
  cur.execute('select snum, sname, type, month, year from masters where advisor=\''+adv+'\' order by year,month desc')
  columns = ['snum','sname','type','month','year']
  answers = []
  rows = cur.fetchall()
  for row in rows:
    answers.append(dict(zip(columns,row)))
  con.close()
  result = {"students":answers}
  return json.dumps(result, indent=2)

def getPhDStudentsGivenAdvisorYear(adv,yr) :
  con = psycopg2.connect(database='grad', user='raj')
  cur = con.cursor()
  cur.execute('select snum, sname, advisor, coadvisor, month from phd where (advisor=\''+adv+'\' or coadvisor=\''+adv+'\') and year = '+str(yr)+' order by year, month')
  columns = ['snum','sname','advisor','coadvisor','month']
  answers = []
  rows = cur.fetchall()
  for row in rows:
    answers.append(dict(zip(columns,row)))
  con.close()
  result = {"students":answers}
  return json.dumps(result, indent=2)

def getMSStudentsGivenAdvisorYear(adv,yr) :
  con = psycopg2.connect(database='grad', user='raj')
  cur = con.cursor()
  cur.execute('select snum, sname, type, month from masters where advisor=\''+adv+
              '\' and year = '+str(yr)+' order by year, month')
  columns = ['snum','sname','type','month']
  answers = []
  rows = cur.fetchall()
  for row in rows:
    answers.append(dict(zip(columns,row)))
  con.close()
  result = {"students":answers}
  return json.dumps(result, indent=2)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/grad/advisors', methods=['GET'])
def get_advisors():
  return getAdvisors()

@app.route('/grad/years', methods=['GET'])
def get_years():
  return getYears()

@app.route('/grad/<string:adv>/<string:deg>', methods=['GET'])
def get_students_given_advisor_degree(adv,deg):
  if deg == "phd":
    return getPhDStudentsGivenAdvisor(adv) 
  elif deg == "ms":
    return getMSStudentsGivenAdvisor(adv)
  else:
    return json.dumps({"error": "Invalid Degree"})

@app.route('/grad/<string:adv>/<string:deg>/<int:yr>', methods=['GET'])
def get_students_given_advisor_degree_year(adv,deg,yr):
  if deg == "phd":
    return getPhDStudentsGivenAdvisorYear(adv,yr) 
  elif deg == "ms":
    return getMSStudentsGivenAdvisorYear(adv,yr)
  else:
    return json.dumps({"error": "Invalid Degree"})

if __name__ == '__main__':
    app.run(host='tinman.cs.gsu.edu',debug=True)
