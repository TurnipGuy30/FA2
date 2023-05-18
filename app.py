from flask import Flask, redirect, render_template, request, url_for
from math import ceil
from werkzeug.wrappers.response import Response

app = Flask(__name__)

input_fields = [
	'fence-length',
	'fence-height',
	'pailing-spacing'
]
output_names = [
	'posts',
	'post_length',
	'post_spacing',
	'rails',
	'rail_length',
	'rows_of_rails',
	'pailings',
	'pailing_length',
	'pailing_width',
	'bags',
	'bags_weight',
	'posts_price',
	'rails_price',
	'pailings_price',
	'bags_price',
	'total_price'
]
prices = {
	# approximate dollars per post (any length)
	'posts': 18.9,
	# approximate dollars per rail (any length)
	'rails': 14.17,
	# approximate dollars per pailing (any length)
	'pailings': 3.8,
	# approximate dollars per concrete bag (20kg)
	'bags': 12.2
}

@app.route('/')
def root() -> Response:
	return redirect(url_for('calculator'))

@app.route('/calculator', methods=['GET', 'POST'])
def calculator() -> str: # sourcery skip: low-code-quality

	inputs = {}
	outputs = {}
	messages = []

	if request.method == 'POST' and all(i in request.form for i in input_fields):
		inputs |= {i: request.form.get(i, None, float) for i in input_fields}
		if any(inputs[i] is None for i in inputs):
			messages.append('Please complete all fields')
		else:
			outputs |= {
				'bags_weight': 20,
				'pailing_length': inputs['fence-height'],
				'pailing_width': 100,
				'post_length': inputs['fence-height'] / 0.75,
				'post_spacing': 2.4,
				'rows_of_rails': 2 if inputs['fence-height'] < 1.2 else 3,
			}
			outputs |= {
				'pailings': ceil(
					inputs['fence-length'] * 100 / (
						outputs['pailing_width'] + (inputs['pailing-spacing'] - 1)
					)
				),
				'rail_length': outputs['post_spacing'],
			}
			outputs |= {
				'posts': ceil(
					inputs['fence-length'] / outputs['rail_length'] + (
						1 if inputs['fence-length'] % outputs['post_spacing']
						> outputs['post_spacing'] / 2 else 0
					)
				)
			}
			outputs |= {
				'bags': ceil(
					outputs['posts']
					* inputs['fence-height']
					* 1.8
				),
				'rails': (outputs['posts'] - 1) * outputs['rows_of_rails'],
			}
			outputs |= {
				'posts_price': '{:,}'.format(
					ceil(outputs['posts'] * prices['posts'])
				),
				'rails_price': '{:,}'.format(
					ceil(outputs['rails'] * prices['rails'])
				),
				'pailings_price': '{:,}'.format(
					ceil(outputs['pailings'] * prices['pailings'])
				),
				'bags_price': '{:,}'.format(
					ceil(outputs['bags'] * prices['bags'])
				)
			}
			outputs |= {
				'total_price': '{:,}'.format(ceil(
					outputs['posts'] * prices['posts']
					+ outputs['rails'] * prices['rails']
					+ outputs['pailings'] * prices['pailings']
					+ outputs['bags'] * prices['bags']
				))
			}
			for key in outputs:
				if type(outputs[key]) == float:
					outputs[key] = '{:,}'.format(round(outputs[key], 2) or 0)
				elif type(outputs[key]) == int:
					outputs[key] = '{:,}'.format(outputs[key] or 0)

	return render_template(
		'calculator.html',
		messages=messages,
		outputs=outputs or {key: 0 for key in output_names}
	)

if __name__ == '__main__':
	app.run(debug=True)
