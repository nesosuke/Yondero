# from flask_login import login_required
from flask import Flask, redirect, render_template, request, url_for, Blueprint
from flask_cors import CORS
bp = Blueprint('web', __name__,
               url_prefix='/web',
               static_folder='static/frontend',
               template_folder='templates/frontend',
               )


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/hello')  # for testing
def hello():
    return 'Hello World!'


# @login_required
@bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


# @login_required
@bp.route('/items', methods=['GET'])
def items():
    return render_template('items.html')


# @login_required
@bp.route('/record', methods=['GET', 'POST'])
def record():
    return render_template('record.html')


@bp.route('/login', methods=['GET'])
def web_login():
    return render_template('login.html')


# @login_required
@bp.route('/logout', methods=['GET'])
def web_logout():
    return render_template('logout.html')


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return redirect(url_for('web.record'))

    if request.files and 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

    return 'File uploaded. File name: %s' % file.filename

    body = request.form['body']
    return body
    # iteminfo = {
    #     'title': body['title'],
    #     'authors': body['authors'],
    #     'year': body['year'],
    #     'journal': body['journal'],
    #     'volume': body['volume'],
    #     'issue': body['issue'],
    #     'pages': body['pages'],
    #     'doi': body['doi'],
    #     'abstract': body['abstract'],
    #     'note': body['note'],
    # }
    # itemfile = body['file']  # bytes

    # TODO: API upload process

    if True:
        return redirect(url_for('web.upload_succeed'))
    else:
        return redirect(url_for('web.web_error'))


@bp.route('/upload_succeed', methods=['GET'])
def upload_succeed():
    return render_template('upload_succeed.html')


@bp.route('/error', methods=['GET'])
def error():
    return render_template('error.html')

@bp.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')
