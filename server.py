from .app import CA_space, Cell
from flask import Flask
from flask import request, render_template, url_for, redirect, jsonify
from flask_expects_json import expects_json
from werkzeug.utils import secure_filename
import json
import os
import datetime
import hashlib


UPLOAD_FOLDER = 'static/temp/'
ALLOWED_EXTENSIONS = set(['txt', 'png'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def delete_temp():
	folder = "static/temp"
	for file in os.listdir(folder):
		file_path = os.path.join(folder, file)
		try:
			if os.path.isfile(file_path):
				os.remove(file_path)
		except Exception as a:
			print(e)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=('GET', 'POST'))
def main_page():
	delete_temp()
	if request.method == 'POST':
		try:
			x = int(request.form.get('x'))
			y = int(request.form.get('y'))
			n = int(request.form.get('n'))

		except TypeError:
			raise InvalidUsage('Wrong data supplied. Please send data via webform.', status_code=400)
		
		if x not in range(2,301) and y not in range(2,301) and n not in range(2,301) and n >= max(x,y):
			raise InvalidUsage('Wrong data supplied.  Please send data via webform.', status_code=400)
		
		CA = CA_space(x,y,n)
		time = str(datetime.datetime.now()).encode('utf-8')
		name = hashlib.sha256(time).hexdigest()
		name = str(name)
		CA.fill_space(name)

		return redirect(url_for('final_page', name=name))

	return render_template('main.html')


@app.route("/import", methods=('GET', 'POST'))
def import_page():
	delete_temp()
	if request.method == 'POST':
		if 'file' not in request.files:
			raise InvalidUsage('Wrong data supplied. Please send data via webform.', status_code=400)
		file = request.files['file']
		if file.filename == '':
			raise InvalidUsage('Wrong data supplied. Please send data via webform.', status_code=400)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(file_path)
			CA = CA_space(2,2,2)
			CA.import_txt(filename)
			time = str(datetime.datetime.now()).encode('utf-8')
			name = hashlib.sha256(time).hexdigest()
			name = str(name)
			CA.fill_space(name)
			return redirect(url_for('final_page', name=name))

	return render_template('import.html')


@app.route("/final/<name>")
def final_page(name):
	if len(os.listdir('static/temp') ) == 0:
		return redirect(url_for('main_page'))
	return render_template('final.html', name=name)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	delete_temp()
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404