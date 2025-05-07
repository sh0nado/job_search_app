from flask import render_template, flash, redirect, url_for
from app import app

@app.route('/')
@app.route('/index')
def index():
    # Placeholder for homepage content
    return "Hello, World!" 