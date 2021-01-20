import os
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, Follows, MovieList, Movie, Comment
from secret_key import key
from api_key import api_key
import requests
import json
from sqlalchemy.exc import IntegrityError
from forms import NewUserForm, UserLoginForm, EditUserForm, NewListForm, NewUserCommentForm
from user_functions import signup, authenticate, is_following, is_followed_by


#k_jg1h63to
CURRENT_USER_KEY = 'current_user'
# Note that you are limited to 100 API calls per day...
base_url = f"https://imdb-api.com/en/API/Search/{api_key}"
cast_url = f"https://imdb-api.com/en/API/FullCast/{api_key}"
wikipedia_url = f"https://imdb-api.com/en/API/Wikipedia/{api_key}"
poster_url = f"https://imdb-api.com/en/API/Posters/{api_key}"

URL_DICTIONARY = {'base': base_url, 'cast': cast_url, 'wiki' : wikipedia_url, 'poster': poster_url}

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
    this_user = None
    
    if CURRENT_USER_KEY in session:
        this_user = User.query.get_or_404(session[CURRENT_USER_KEY])

    return render_template('homepage.html', this_user=this_user)


@app.route('/signup', methods=['GET', 'POST'])
def signup_():
    form = NewUserForm()

    if form.validate_on_submit():
        try:
            this_user = signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                user_pic_url=form.user_pic_url.data or User.user_pic_url.default.arg
            )
            
            db.session.add(this_user)
            db.session.commit()
        
        except IntegrityError:
            flash('Username already taken', 'danger')
            return render_template('/signup_and_login/signup.html', form=form)
        
        do_login(this_user)
        flash(f"Welcome to MovieBuddy, {this_user.username}", 'success')
        return redirect(f"/users/{this_user.id}")
    
    
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
    res = requests.get(f"http://127.0.0.1:5000/api/get-movie-details/base/{title}") # Only works locally; fix this to accomodate bothe cases 
    res = json.loads(res.text)['results']

    return render_template('search/show-query-results.html', res=res, query=title, this_user=this_user)


@app.route('/show-movie-details/<string:id>')
def show_movie_details(id):
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    
    res = requests.get(f"http://127.0.0.1:5000/api/get-movie-details/cast/{id}") # Only works locally
    res = json.loads(res.text)

    wiki_response = requests.get(f"http://127.0.0.1:5000/api/get-movie-details/wiki/{id}") # only works locally
    wiki_response = json.loads(wiki_response.text)
    
    poster_response = requests.get(f"http://127.0.0.1:5000/api/get-movie-details/poster/{id}")
    poster_response = json.loads(poster_response.text)
    
    return render_template('show-movie-details.html', title=res['fullTitle'], 
        directors=res['directors'], 
        writers=res['writers'],
        actors=res['actors'][:10],
        plot=wiki_response['plotShort'],
        poster=poster_response['posters'][0]['link'],
        this_user=this_user)


@app.route('/users/<int:id>')
def show_user_profile(id):
    user = User.query.get_or_404(id)
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return render_template('user/show_profile_details.html', user=user, this_user=this_user)


@app.route('/users/<int:id>/show-lists', methods=['GET'])
def show_user_lists(id):
    user = User.query.get_or_404(id)
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    
    return render_template('user/show_user_lists.html', user=user, this_user=this_user)


@app.route('/users/<int:id>/following', methods=['GET']) # todo
def show_user_following(id):
    user = User.query.get_or_404(id)
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return render_template('user/following.html', user=user, this_user=this_user, is_following=is_following)


@app.route('/users/<int:id>/followers', methods=['GET']) # todo
def show_user_followers(id):
    user = User.query.get_or_404(id)
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return render_template('user/followers.html', user=user, this_user=this_user, is_following=is_following)


@app.route('/users/new-list', methods=['GET', 'POST']) # todo
def make_new_movie_list():
    form = NewListForm()
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    
    if form.validate_on_submit():
        try:
            new_list = MovieList(
                owner=this_user.id,
                title=form.title.data,
                description=form.description.data,
                list_image_url=form.list_image_url.data
            )
            
            db.session.add(new_list)
            db.session.commit()
        
        except IntegrityError:
            flash('Generic Error Message For Now (come back)', 'danger')
        
        return redirect(f"/users/{this_user.id}/show-lists")
        
    return render_template('lists/new_movie_list_form.html', this_user=this_user, form=form)


@app.route('/users/<int:id>/edit-profile', methods=['GET', 'POST'])
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


@app.route('/users/follow/<int:follow_id>', methods=['POST'])
def add_follow(follow_id):
    
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    followed_user = User.query.get_or_404(follow_id)
    this_user.following.append(followed_user)
    db.session.commit()

    return redirect(f"/users/{this_user.id}/following")


@app.route('/users/stop-following/<int:followed_user_id>', methods=['POST'])
def unfollow(followed_user_id):
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    followed_user = User.query.get_or_404(followed_user_id)
    this_user.following.remove(followed_user)
    db.session.commit()
    
    return redirect(f"/users/{this_user.id}/following")


@app.route('/users/<int:user_id>/lists/<int:list_id>/details')
def show_user_list_details(user_id, list_id):
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    user = User.query.get_or_404(user_id)
    movie_list = MovieList.query.get_or_404(list_id)
    return render_template('lists/show_user_list.html', user=user,this_user=this_user,movie_list=movie_list)
    
    
@app.route('/users/delete/<int:movie_list_id>', methods=['GET', 'DELETE'])
def delete_movie_list(movie_list_id):
    movie_list = MovieList.query.get_or_404(movie_list_id)
    user_id = movie_list.owner
    
    db.session.delete(movie_list)
    db.session.commit()
    
    return redirect(f"users/{user_id}")
#-------------------------------------------------------------------------
#                         External API calls

@app.route('/api/get-movie-details/<string:type>/<string:query>', methods=['GET'])
def get_movie_details(query, type):
    res = requests.get(f"{URL_DICTIONARY[type]}/{query}").text
    return jsonify(json.loads(res))