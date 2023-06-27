from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder='site_template')

@site.route('/')
def home():
    print('look at this cool project. Would you just look at it')
    return render_template('index.html')