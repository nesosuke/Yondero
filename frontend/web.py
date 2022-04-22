from crypt import methods
# from flask_login import login_required
from flask import Flask, render_template, url_for, Blueprint
from flask_cors import CORS

bp = Blueprint('web', __name__,
               url_prefix='/web',
               static_folder='static/frontend',
               template_folder='templates/frontend',
               )


@bp.route('/')
def web_index():
    return render_template('index.html')


@bp.route('/hello')  # for testing
def web_hello():
    return 'Hello World!'


# @login_required
@bp.route('/dashboard', methods=['GET'])
def web_dashboard():
    return render_template('dashboard.html')


# @login_required
@bp.route('/items', methods=['GET'])
def web_items():
    return render_template('items.html')


# @login_required
@bp.route('/record', methods=['GET'])
def web_record():
    return render_template('record.html')


# @login_required
@bp.route('/record', methods=['POST'])
def web_record_post():
    return render_template('record.html')


@bp.route('/login', methods=['GET'])
def web_login():
    return render_template('login.html')


# @login_required
@bp.route('/logout', methods=['GET'])
def web_logout():
    return render_template('logout.html')
