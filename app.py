from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

import os
import xlrd
from math import ceil

UPLOAD_FOLDER = 'example'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

name_file = []
files = []
tables = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', "POST"])
def index():
    return render_template('home.html', files=files, tables=tables, filename=name_file)

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name_file.append(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            files.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            get_table(filename)
            return redirect(url_for('index'))
    return redirect(url_for('index')) % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

@app.route('/table', methods=['POST'])
def get_table(filename):
    if request.method == 'POST':
        workbook = xlrd.open_workbook(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        worksheet = workbook.sheet_by_index(0)
        table = []
        for row in range(worksheet.nrows):
            for col in range(worksheet.ncols):
                table.append(worksheet.cell_value(row, col))
        t = ceil(len(table)/8)
        tables.append([table[t*k:t*(k+1)] for k in range(8)])
        print(tables)
        return redirect(url_for('index'))
    return redirect(url_for('index')) 

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run(port=2019,debug=True)
