from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_material import Material



blueprint = Blueprint('blueprint', __name__)



@blueprint.route('/')
def index():
    return 'Hello World!'
