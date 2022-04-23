# from flask_login import login_required
from email import message
from re import U
from flask import (Blueprint, Flask, redirect, render_template, request,
                   url_for)
from flask_cors import CORS
from werkzeug.utils import secure_filename
import requests
bp = Blueprint('web', __name__,
               url_prefix='/web',
               static_folder='static/frontend',
               template_folder='templates/frontend',
               )
attachments_file_savedir = './attachments'
api_url = 'http://localhost:8080/api/v1'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# test data
user = {
    'username': 'test',
    'email': 'test@example.com',
}
session = {
    'session_id': 1,
    'user_id': 1,
}
stats = {
    'total': 100,
    'starrted': 10,
    'unread': 10,
}
itemdata = {
    'title': 'test title',
    'authors': ['author1', 'author2'],
    'year': '2020',
    'journal': 'test journal',
    'volume': '42',
    'issue': '1',
    'pages': '1-2',
    'doi': '10.9999/test.doi',
    'abstract': 'lorem ipsum',
    'note': 'lorem ipsum lorem ipsum note',
}
# end of test data

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_user_id_from_session(session_id):
    # TODO get session id from Flask.LoginManager

    user_id = 1  # TODO get user id from session id
    return user_id


def get_stats(user_id):
    user_id = str(user_id)
    url = api_url+'/users/'+user_id
    token = 1  # TODO get token from Flask.LoginManager
    token = str(token)
    headers = {
        'user_id': user_id,
        'token': token,
    }
    # TODO get stats from API
    res = requests.get(url, headers=headers).json()

    stats = {
        'total_count': res['total_count'],
        'starrted_count': res['starrted_count'],
        'unread_count': res['unread_count'],
    }

    return stats


def get_userdata(user_id):
    user_id = str(user_id)
    url = api_url+'/users/'+user_id
    token = 1  # TODO get token from Flask.LoginManager
    token = str(token)
    headers = {
        'user_id': user_id,
        'token': token,
    }
    # TODO get user data from API
    res = requests.get(url, headers=headers).json()

    userdata = {
        'username': res['username'],
        'email': res['email'],
        'avatar': res['avatar'],
    }
    return userdata


@bp.route('/')
def index():
    return render_template('index.html',user=user)


@bp.route('/hello')  # for testing
def hello():
    return 'Hello World!'


# @login_required
@bp.route('/dashboard', methods=['GET'])
def dashboard():
    # TODO get session id from Flask.LoginManager
    # user_id = get_user_id_from_session(1)
    # userdata = get_userdata(user_id)
    # stats = get_stats(user_id)

    return render_template('dashboard.html', user=user, stats=stats)


# @login_required
@bp.route('/items', methods=['GET'])
def items():
    '''
    show list of items
    '''
    return render_template('items.html',user=user)


@bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html',user=user)


# @login_required
@bp.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('web.index'))


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    '''
    upload file and metadata to server
    '''

    if request.method == 'GET':
        return render_template('upload.html',user=user)

    # metadata handling
    body = request.form


    session_key = 1  # TODO: get session_key from session

    # post metadata to server
    res = requests.post(api_url+'/items', json=itemdata,
                        headers={'session_key': session_key})
    if res.status_code == 200:
        result_item = 'item added successfully'
    else:
        result_item = 'item add failed'
        # metadata is somehow wrong
        return render_template('error.html', message=result_item)

    # file handling
    if request.files:  # if there is a file
        file = request.files['file']
        if file and allowed_file(file.filename):  # file is allowed
            filename = secure_filename(file.filename)
            # post file to server
            res = requests.post(
                api_url+'/attachments', files={'file': file}, headers={'session_key': session_key})
            if res.status_code == 200:
                result_file = 'file added successfully'
            else:
                result_file = 'file add failed'
                return render_template('error.html', message=result_file, user=user)

        elif file.filename == '':  # no file selected
            result_file = 'empty filename is not allowed'
            return render_template('error.html', message=result_file, user=user)

        else:  # file is not allowed
            result_file = 'file type is not allowed'
            return render_template('error.html', message=result_file, user=user)
    else:  # no file
        pass        # do nothing

    # upload finish successfully
    if 'successfully' in result_file and 'successfully' in result_item:
        return render_template('success.html', message='upload successfully', user=user)
    else:
        return render_template('error.html', message='upload failed', user=user)


@bp.route('/download', methods=['GET'])
def download():
    '''
    download file from server
    '''

    # TODO: get item_id from request
    item_id = 1
    # TODO: get session_key from request
    session_key = 1
    # TODO: get file from server
    pass


@bp.route('/error', methods=['GET'])
def error(message):
    return render_template('error.html',user=user,message=message)


@bp.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html',user=user)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html',user=user)
