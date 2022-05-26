

import glob
import os
import warnings
import textract
import requests
from flask import (Flask, session, g, json, Blueprint, flash, jsonify, redirect, render_template, request,
                   url_for, send_from_directory)
from gensim.summarization import summarize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
import pdf2txt as pdf
import PyPDF2

import screen
import search
import hashlib

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)

app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    USERNAME='admin',
    PASSWORD='20ddfa0d4a5efdeabf0d56a52a21151b',
    SECRET_KEY='development key',
))


app.config['UPLOAD_FOLDER'] = 'Original_Resumes/'
app.config['ALLOWED_EXTENSIONS'] = set(
    ['text', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class jd:
    def __init__(self, name):
        self.name = name


def getfilepath(loc):
    temp = str(loc).split('\\')
    return temp[-1]


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif app.config['PASSWORD'] != hashlib.md5(request.form['password'].encode('utf-8')).hexdigest():
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


@app.route('/')
def home():
    x = []
    for file in glob.glob("/home/test/Desktop/Automated-Resume-Ranking-System/Job_Description/*.txt"):
        res = jd(file)
        x.append(jd(getfilepath(file)))
    print(x)
    return render_template('index.html', results=x)


@app.route('/results', methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        jobfile = request.form['des']
        print(jobfile)
        print("nicely done......flag1")
        flask_return = screen.res(jobfile)
        print(flask_return)
        return render_template('result.html', results=flask_return)


@app.route('/resultscreen',  methods=['POST', 'GET'])
def resultscreen():
    if request.method == 'POST':
        jobfile = request.form.get('Name')
        print(jobfile)
        flask_return = screen.res(jobfile)
        return render_template('result.html', results=flask_return)


@app.route('/resultsearch', methods=['POST', 'GET'])
def resultsearch():
    if request.method == 'POST':
        search_st = request.form.get('Name')
        print(search_st)
    result = search.res(search_st)
    # return result
    return render_template('result.html', results=result)


@app.route('/Original_Resume/<path:filename>')
def custom_static(filename):
    return send_from_directory('./Original_Resumes', filename)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True, threaded=True)
