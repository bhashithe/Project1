from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
	return '<h1>hello world</h1>'

if __name__ == '__main__':
	app.run(debug=True, port=5028)
