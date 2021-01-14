import os
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, Follows
from secret_key import key
from api_key import api_key
import requests
import json
from sqlalchemy.exc import IntegrityError
from forms import NewUserForm, UserLoginForm
from user_functions import signup, authenticate

#k_jg1h63to


CURRENT_USER_KEY = 'current_user'
# Note that you are limited to 100 API calls per day...
base_url = f"https://imdb-api.com/en/API/Search/{api_key}"
cast_url = f"https://imdb-api.com/en/API/FullCast/{api_key}"
wikipedia_url = f"https://imdb-api.com/en/API/Wikipedia/{api_key}"

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
    if CURRENT_USER_KEY in session:
        user = User.query.get_or_404(session[CURRENT_USER_KEY])
    else:
        user = None
        
    return render_template('homepage.html', user=user)


@app.route('/signup', methods=['GET', 'POST'])
def signup_():
    form = NewUserForm()

    if form.validate_on_submit():
        try:
            user = signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                user_pic_url=form.user_pic_url.data or User.user_pic_url.default.arg
            )
            
            db.session.add(user)
            db.session.commit()
        
        except IntegrityError:
            flash('Username already taken', 'danger')
            return render_template('/signup_and_login/signup.html', form=form)
        
        do_login(user)
        flash(f"Welcome to MovieBuddy, {user.username}", 'success')
        return redirect(f"/users/{user.id}")
    
    
    return render_template('/signup_and_login/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    
    if form.validate_on_submit():
        user = authenticate( form.username.data, form.password.data)
        if user:
            do_login(user)
            flash(f"Welcome back {user.username}", 'success')
            return redirect(f"/users/{user.id}")
        
        flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('/signup_and_login/login.html', form=form) 


@app.route('/logout')
def logout():
    user = User.query.get_or_404(session[CURRENT_USER_KEY])
    do_logout()
    
    return redirect('/')


@app.route('/get-movie-by-query', methods=['GET'])
def get_move_by_query():
    user = User.query.get_or_404(session[CURRENT_USER_KEY])
    title = request.args.get('q') # just assume the query is a title for now
    res = requests.get(f"http://127.0.0.1:5000/api/get-movie-by-title/{title}") # Only works locally; fix this to accomodate bothe cases 
    res = json.loads(res.text)['results']
    # print(f"----------------------------------\n{res}\n--------------------------------------")
    return render_template('search/show-query-results.html', res=res, query=title, user=user)


@app.route('/show-movie-details/<string:id>')
def show_movie_details(id):
    user = User.query.get_or_404(session[CURRENT_USER_KEY])
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

    plot = wiki_response['plotShort']
    
    return render_template('show-movie-details.html', title=full_title, 
        directors=directors, 
        writers=writers,
        actors=actors,
        plot=plot,
        user=user)


@app.route('/users/<int:id>')
def show_users_own_profile(id):
    user = User.query.get_or_404(session.get(CURRENT_USER_KEY))
    return render_template('user/show_profile_details.html', user=user)


@app.route('/users/<int:id>/my-lists', methods=['GET'])
def show_user_lists(id):
    user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return render_template('user/show_user_lists.html', user=user)


@app.route('/users/<int:id>/following', methods=['GET']) # todo
def show_user_following(id):
    user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return render_template('user/following.html', user=user)


@app.route('/users/<int:id>/followers', methods=['GET']) # todo
def show_user_followers(id):
    user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return render_template('user/followers.html', user=user)

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