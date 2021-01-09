import os
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db
from secret_key import key
from api_key import api_key

CURRENT_USER_KEY = 'current_user'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///movie_app_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', key)
toolbar = DebugToolbarExtension(app)

db.app = app
db.init_app(app)


def do_login(user):
    session[CURRENT_USER_KEY] = user.id


def do_logout():
    if CURRENT_USER_KEY in session:
        del session[CURRENT_USER_KEY]
        
@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/get-move-by-query')
def get_move_by_query():
    title = request.args.get('search-query') # just assume the query is a title for now
    res =  requests.get() # Pick up here. Need the base URL. Set it at the top


@app.route('/api/get-movie-by-title', methods=["GET"])
def get_movie_my_title(title):
    return jsonify('your mom')
