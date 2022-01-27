"""Instruction how to upload files https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/"""

import os
from flask import Flask, session, Blueprint, flash, current_app, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from template_autofill import src
from datetime import datetime


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'instance', 'uploaded_files')
RESULTS_FOLDER = os.path.join(os.getcwd(), 'instance', 'processed_files')
RESULTS_ZIP_FOLDER = os.path.join(os.getcwd(), 'instance', 'zip_archive')


FILLED_ONE_PPT = 'filled_one_ppt.pptx'
FILLED_SEPARATE_PPT = 'filled_separate_ppt'
FILLED_ONE_PDF = 'filled_one_pdf.pdf'


bp = Blueprint("routes", __name__)


def get_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")


@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    
    if request.method == 'POST':
        
        if ('file1' not in request.files) or ('file2' not in request.files):
            return redirect(request.url)
        
        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1 and file2:
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            file1.save(os.path.join(UPLOAD_FOLDER, filename1))
            file2.save(os.path.join(UPLOAD_FOLDER, filename2))
            
            try:
                
                pres = src.read_presentation(os.path.join(UPLOAD_FOLDER, filename1))
                data = src.read_data(os.path.join(UPLOAD_FOLDER, filename2))
                new_pres = src.fill_pres_with_data(pres, data)
                src.save_presentation(new_pres, os.path.join(RESULTS_FOLDER, FILLED_ONE_PPT))
                
                src.fill_sep_pres_with_data(pres, data, os.path.join(RESULTS_FOLDER))
                src.save_files_as_zip(os.path.join(RESULTS_FOLDER), os.path.join(RESULTS_ZIP_FOLDER, FILLED_SEPARATE_PPT))
                
            except Exception as e:
                flash(str(e))
                return redirect(url_for('routes.upload_file'))
            
            return redirect(url_for('routes.download_file', name=FILLED_SEPARATE_PPT+'.zip'))
        
    return render_template('index.html')
    

@bp.route('/download_file/<name>')
def download_file(name):
    return send_from_directory(RESULTS_ZIP_FOLDER, name)
