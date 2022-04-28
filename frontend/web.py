from flask import Blueprint, render_template

bp = Blueprint('web', __name__,
               url_prefix='/web',
               static_folder='static/frontend',
               template_folder='templates/frontend',
               )


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/documents', methods=['GET', 'POST'])
def documents_all():
    return render_template('documents_all.html')


@bp.route('documents/<document_id>', methods=['GET', 'PUT', 'DELETE'])
def document(document_id):
    return render_template('document.html', document_id=document_id)


@bp.route('/documets/<document_id>/file', methods=['GET', 'POST', 'PUT', 'DELETE'])
def document_file(document_id):
    return render_template('document_file.html', document_id=document_id)
