"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask.json import jsonify
from DAPI import app
import pyodbc as pypyodbc

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
    conn = pypyodbc.connect(driver='{SQL Server}', server='localhost', database='ZocData')

    cur = conn.cursor()
    cur.execute('select personId, firstName, lastName from person where personId = %s' % person_id)
    row = cur.fetchone()

    return jsonify(personId=row[0],
                   firstName=row[1],
                   lastName=row[2])
    #return render_template(
    #    'doctor.html',
    #    title='Doctor Info',
    #    year=datetime.now().year,
    #    person_id=row[0],
    #    name=row[2]+' '+row[3]+' '+row[4]
    #)