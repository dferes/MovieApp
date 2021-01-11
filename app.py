import os
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db
from secret_key import key
from api_key import api_key
import requests
import json

CURRENT_USER_KEY = 'current_user'
# Note that you are limited to 100 API calls per day...
base_url = f"https://imdb-api.com/en/API/Search/{api_key}"
cast_url = f"https://imdb-api.com/en/API/FullCast/{api_key}"
wikipedia_url = f"https://imdb-api.com/en/API/Wikipedia/{api_key}" # followed by imdb id

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


@app.route('/get-movie-by-query', methods=['GET'])
def get_move_by_query():
    title = request.args.get('q') # just assume the query is a title for now
    res = requests.get(f"http://127.0.0.1:5000/api/get-movie-by-title/{title}") # Only works locally; fix this to accomodate bothe cases 
    res = json.loads(res.text)['results']
    # print(f"----------------------------------\n{res}\n--------------------------------------")
    return render_template('search/show-query-results.html', res=res, query=title)


@app.route('/show-movie-details/<string:id>')
def show_movie_details(id):
    # print(f"The ID is: {id}")
    res = requests.get(f"http://127.0.0.1:5000/api/get-cast-information/{id}") # Only works locally
    res = json.loads(res.text)
    # print('---------------------------------',res, '------------------------------')
    # for key, val in res.items():
    #     print(f"    {key}: {val}")
    #     print("\n")
    full_title = res['fullTitle']
    directors = res['directors']
    writers = res['writers']
    actors = res['actors'][:10] # limit relavent actors to top 10 for now
    # print('ACTORS:\n\n', actors, '\n')
    # print('DIRECTORS:\n\n', directors, '\n')
    # print('WRITERS:\n\n', writers, '\n')
    wiki_response = requests.get(f"http://127.0.0.1:5000/api/get-wikipedia-information/{id}") # only works locally
    wiki_response = json.loads(wiki_response.text)
    # for key in wiki_response.keys():
    #     print(f"{key}\n\n")
    print('--------------------------------------')
    print(wiki_response['url'])
    plot = wiki_response['plotShort']
    
    return render_template('show-movie-details.html', title=full_title, 
        directors=directors, 
        writers=writers,
        actors=actors,
        plot=plot)


#-------------------------------------------------------------------------
#                         External API calls


@app.route('/api/get-movie-by-title/<string:title>', methods=['GET'])
def get_movie_my_title(title):
    res = requests.get(f"{base_url}/{title}").text
    return jsonify(json.loads(res))


@app.route('/api/get-cast-information/<string:id>', methods=['GET'])
def get_full_cast_information(id):
    res = requests.get(f"{cast_url}/{id}").text
    return jsonify(json.loads(res))


@app.route('/api/get-wikipedia-information/<string:id>', methods=['GET'])
def get_wikipedia_information(id):
    res = requests.get(f"{wikipedia_url}/{id}").text
    return jsonify(json.loads(res))