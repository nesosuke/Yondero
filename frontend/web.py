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
