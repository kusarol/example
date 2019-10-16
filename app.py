import os
from constants import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from tables import table, get_table, get_names

from flask import Flask, request, \
                render_template, send_from_directory
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            rows = table(os.path.join(app.config['UPLOAD_FOLDER'],
                         filename), filename)
            files = get_names()
            table_find = get_table(filename.replace('.xls', ''))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('home.html', tables=rows,
                           files=files, get_table=table_find)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/my-link/')
def get_upload_table(filename):
    table_find = get_table(filename.replace('.xls', ''))
    return render_template('home.html', get_table=table_find)


if __name__ == "__main__":
    app.run(port=2019, debug=True)
