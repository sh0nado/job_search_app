from flask import render_template, flash, redirect, url_for
from app import app
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', year=datetime.now().year) 