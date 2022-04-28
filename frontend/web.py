import requests
from flask import Blueprint, Flask, redirect, render_template, request, url_for
from flask_cors import CORS

bp = Blueprint('web', __name__,
               url_prefix='/web',
               static_folder='static/frontend',
               template_folder='templates/frontend',
               )
api_url = 'http://localhost:8080/api/v1'

# test data
data = {
    "doi": "10.2307/1969529",
    "document_type": "article",
    "title": "Non-Cooperative Games",
    "authors": [
        "John Nash"
    ],
    "journal": "Annals of Mathematics",
    "volume": "54",
    "issue": "2",
    "pages": "286--295",
    "year": "1951",
    "abstract": "This is an abstract",
    "keywords": [
        "keyword1",
        "keyword2"
    ],
    "url": "http://www.jstor.org/stable/1969529",
    "note": "This is a note",
    "tags": [
        "tag1",
        "tag2"
    ]
}
# end of test data


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
