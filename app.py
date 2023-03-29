from flask import Flask, redirect, render_template, request, url_for
from werkzeug.wrappers.response import Response

app = Flask(__name__)

@app.route('/')
def root() -> Response:
	return redirect(url_for('calculator'))

@app.route('/calculator')
def calculator() -> str:
	return render_template('calculator.html')

if __name__ == '__main__':
	app.run(debug=True)
