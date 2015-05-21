"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask.json import jsonify
from DAPI import app
from DAPI.persistence.db_doc import DocDB

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/api/doctor/<person_id>')
def get_doctor(person_id):

    try:
        doc_db = DocDB()
        doctor = doc_db.get_doctor_by_person_id(person_id)

    except err:
        print ('Failed to retrieve doctor information.. :(')

    return jsonify(doctor)