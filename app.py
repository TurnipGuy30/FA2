from flask import Flask, redirect, render_template, request, url_for
from math import ceil
from werkzeug.wrappers.response import Response

app = Flask(__name__)

input_fields = [
	'fence-length',
	'fence-height',
	'post-spacing',
	'pailing-width',
	'pailing-spacing'
]
output_names = [
	'posts',
	'post_spacing',
	'rails',
	'rail_length',
	'rows_of_rails',
	'pailings',
	'pailing_length',
	'posts_price',
	'rails_price',
	'pailings_price',
	'total_price'
]

@app.route('/')
def root() -> Response:
	return redirect(url_for('calculator'))

@app.route('/calculator', methods=['GET', 'POST'])
def calculator() -> str:

	inputs = {}
	outputs = {}
	messages = []

	if request.method == 'POST' and all(i in request.form for i in input_fields):
		for item in input_fields:
			inputs[item] = request.form.get(item, None, float)
		if any(not inputs[i] for i in inputs):
			messages.append('Please fill out all input fields')
		else:
			outputs |= {
				'posts': None,
				'post_spacing': None,
				'rails': None,
				'rail_length': None,
				'rows_of_rails': None,
				'pailings': None,
				'pailing_length': None,
				'posts_price': None,
				'rails_price': None,
				'pailings_price': None,
				'total_price': None
			}
			for key in outputs:
				outputs[key] = outputs[key] or '-'

	return render_template(
		'calculator.html',
		messages=messages,
		outputs=outputs or {key: '-' for key in output_names},
	)

if __name__ == '__main__':
	app.run(debug=True)
