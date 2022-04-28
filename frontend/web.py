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

# end of test data
