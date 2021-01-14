import os
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, Follows, MovieList
from secret_key import key
from api_key import api_key
import requests
import json
from sqlalchemy.exc import IntegrityError
from forms import NewUserForm, UserLoginForm, EditUserForm, NewListForm
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
        

def update_user_data(form, user):
    user.bio = form.bio.data if form.bio.data else user.bio
    user.header_image_url = form.header_image_url.data if form.header_image_url.data else user.header_image_url
    user.username = form.username.data if form.username.data else user.username
    user.email = form.email.data if form.email.data else user.email
    user.user_pic_url = form.user_pic_url.data if form.user_pic_url.data else user.user_pic_url
    

def pre_populate_user_edit_form_fields(form, user):
    form.username.data = user.username
    form.email.data = user.email
    form.user_pic_url.data = user.user_pic_url if user.user_pic_url != user.user_pic_url[0:7] != '/static' else None 
    form.bio.data = user.bio if user.bio else None
        

@app.route('/')
def homepage():
    if CURRENT_USER_KEY in session:
        this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    else:
        this_user = None
        
    return render_template('homepage.html', this_user=this_user)


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
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    title = request.args.get('q') # just assume the query is a title for now
    res = requests.get(f"http://127.0.0.1:5000/api/get-movie-by-title/{title}") # Only works locally; fix this to accomodate bothe cases 
    res = json.loads(res.text)['results']
    # print(f"----------------------------------\n{res}\n--------------------------------------")
    return render_template('search/show-query-results.html', res=res, query=title, this_user=this_user)


@app.route('/show-movie-details/<string:id>')
def show_movie_details(id):
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
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
        this_user=this_user)


@app.route('/users/<int:id>')
def show_user_profile(id):
    user = User.query.get_or_404(id)
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return render_template('user/show_profile_details.html', user=user, this_user=this_user)


@app.route('/users/<int:id>/my-lists', methods=['GET'])
def show_user_lists(id):
    user = User.query.get_or_404(id)
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return render_template('user/show_user_lists.html', user=user, this_user=this_user)


@app.route('/users/<int:id>/following', methods=['GET']) # todo
def show_user_following(id):
    user = User.query.get_or_404(id)
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return render_template('user/following.html', user=user, this_user=this_user)


@app.route('/users/<int:id>/followers', methods=['GET']) # todo
def show_user_followers(id):
    user = User.query.get_or_404(id)
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return render_template('user/followers.html', user=user, this_user=this_user)


@app.route('/users/new-list', methods=['GET', 'POST']) # todo
def make_new_movie_list():
    form = NewListForm()
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    
    if form.validate_on_submit():
        try:
            new_list = MovieList(
                owner=this_user.id,
                title=form.title.data,
                description=form.description.data
            )
            
            db.session.add(new_list)
            db.session.commit()
        
        except IntegrityError:
            flash('Generic Error Message For Now', 'danger')
        
    return render_template('lists/new_movie_list_form.html', this_user=this_user, form=form)


@app.route('/users/<int:id>/edit-profile', methods=['GET', 'POST']) # POST or PATCH, some of the info is new, some is being replaced..
def edit_user_profile(id):
    form = EditUserForm()
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    
    if form.validate_on_submit():
        update_user_data(form, this_user) 
        
        if authenticate(this_user.username, form.password.data):        
            db.session.add(this_user)
            db.session.commit()
            flash('Your account has been updated.', 'success')
        else:
            flash('Incorrect password.', 'danger')
        
        return redirect(f"/users/{this_user.id}")
    
    pre_populate_user_edit_form_fields(form, this_user)
    
    return render_template('user/edit_profile.html', this_user=this_user, form=form)


@app.route('/users/delete', methods=['GET', 'DELETE'])
def delete_user():
    user = User.query.get_or_404(session[CURRENT_USER_KEY])
    do_logout()

    db.session.delete(user)
    db.session.commit()

    return redirect("/")
#-------------------------------------------------------------------------
#                         External API calls

# Refactor these into one function

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