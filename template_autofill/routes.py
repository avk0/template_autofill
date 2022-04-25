"""Instruction how to upload files https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/"""

import os
import shutil
import io
from tempfile import mkdtemp

from flask import after_this_request, Flask, session, Blueprint,\
                  flash, current_app, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from template_autofill import src
from datetime import datetime
from random import randint


LOG_FOLDER = os.path.join(current_app.instance_path, 'log')

RESULTS_ZIP_FOLDER = os.path.join(current_app.instance_path, 'zip_archive')


FILLED_ONE_PPT = 'filled_one_ppt.pptx'
FILLED_SEPARATE_PPT = 'filled_separate_ppt'
FILLED_ONE_PDF = 'filled_one_pdf.pdf'

SUPPORTED_LANG = ['en', 'ru']

bp = Blueprint("routes", __name__)


def get_timestamp():
    return datetime.now().strftime("%Y.%m.%d_%H.%M.%S")


def recursive_dir_size(path):
    size = 0
    for x in os.listdir(path):
        if not os.path.isdir(os.path.join(path, x)):
            size += os.stat(os.path.join(path, x)).st_size
        else:
            size += recursive_dir_size(os.path.join(path, x))
    return size


def remove_folder(dir_path):
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


@bp.route('/')
def index():

    lang = 'en'
    if request.accept_languages:
        lang = request.accept_languages.best_match(SUPPORTED_LANG)
    return redirect(url_for('routes.upload_file', lang=lang))


@bp.route('/<lang>', methods=['GET', 'POST'])
def upload_file(lang):

    if request.method == 'POST':
        
        if ('file1' not in request.files) or ('file2' not in request.files):
            return redirect(request.url)
        
        file1 = request.files['file1']
        file2 = request.files['file2']

        log_folder_size = recursive_dir_size(LOG_FOLDER)
        while log_folder_size > 10**9:
            dir_path = os.path.join(LOG_FOLDER, min(os.listdir(LOG_FOLDER)))
            remove_folder(dir_path)
            log_folder_size = recursive_dir_size(LOG_FOLDER)

        upload_folder = os.path.join(current_app.instance_path, 'log', get_timestamp())
        os.makedirs(upload_folder, exist_ok=True)
        session['folder'] = upload_folder
        session.modified = True

        # results_folder = os.path.join(upload_folder, f'{randint(1, 1024)}')
        # os.makedirs(results_folder, exist_ok=True)

        if file1 and file2:
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            file1.save(os.path.join(upload_folder, filename1))
            file2.save(os.path.join(upload_folder, filename2))

            tmp_dir = mkdtemp()
            preprocess_folder = os.path.join(tmp_dir, 'preprocess')
            os.makedirs(preprocess_folder, exist_ok=True)
            zip_folder = os.path.join(tmp_dir, 'zip')
            os.makedirs(zip_folder, exist_ok=True)

            try:
                pres = src.read_presentation(os.path.join(session['folder'], filename1))
                data = src.read_data(os.path.join(session['folder'], filename2))
                new_pres = src.fill_pres_with_data(pres, data)
                src.save_presentation(new_pres, os.path.join(preprocess_folder, FILLED_ONE_PPT))
                src.fill_sep_pres_with_data(pres, data, preprocess_folder)
                src.save_files_as_zip(preprocess_folder, os.path.join(zip_folder, FILLED_SEPARATE_PPT))
            except Exception as e:
                flash(str(e))
                return redirect(url_for('routes.upload_file', lang=lang))

            return redirect(url_for('routes.download_file', tmp_dir=tmp_dir))
        
    return render_template(f'index1_{lang}.html')
    

@bp.route('/download_file/<tmp_dir>')
def download_file(tmp_dir):
    mem = io.BytesIO()
    with open(os.path.join(tmp_dir, 'zip', FILLED_SEPARATE_PPT+'.zip'), "rb") as file:
        mem = io.BytesIO(file.read(-1))

    remove_folder(tmp_dir)

    try:
        return send_file(
            mem,
            as_attachment=False,
            attachment_filename='test.zip',
            mimetype='zip'
        )
        # return send_from_directory(os.path.join(tmp_dir, 'zip'), path=FILLED_SEPARATE_PPT+'.zip')
    except FileNotFoundError:
        abort(404)