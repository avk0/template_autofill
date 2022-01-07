import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

import src

UPLOAD_FOLDER = './uploaded_temp'
FILLED_PPTX = 'filled template.pptx'
ALLOWED_EXTENSIONS = {'pptx', 'xlsx'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        if ('file1' not in request.files) or ('file2' not in request.files):
            print('dd')
            flash('No file part')
            return redirect(request.url)
        
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        if (file1.filename == '') or (file2.filename == ''):
            print('ss')
            flash('No selected file')
            return redirect(request.url)
        
        if file1 and file2:
            print('sss')
            flash('Files seen!')
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

            print('ad')

            pres = src.read_presentation(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            data = src.read_data(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            print('aa')
            new_pres = src.fill_pres_with_data(pres, data)
            src.save_presentation(new_pres, os.path.join(app.config['UPLOAD_FOLDER'], FILLED_PPTX))
            print('cc')
            
            return redirect(url_for('download_file', name=FILLED_PPTX))
        
    return render_template('index1.html')


app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
