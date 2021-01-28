import os
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, MovieList, Movie, Comment
from secret_key import key
import requests
import json
from forms import NewUserForm, UserLoginForm, EditUserForm, NewListForm, NewUserCommentForm, EditListForm
from user_functions import authenticate, is_following
from utility_functions import retrieve_movie_details, URL_DICTIONARY, prepopulate_edit_list_form, update_movie_list_data, validate_and_edit_profile
from utility_functions import add_movie_to_list, validate_and_signup, validate_and_create_movie_list, pre_populate_user_edit_form_fields
from recommendation_functions import UserMovieRecommendations

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///movie_app_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', key)
toolbar = DebugToolbarExtension(app)

db.app = app
db.init_app(app)

CURRENT_USER_KEY = 'current_user'
        

def do_login(user):
    session[CURRENT_USER_KEY] = user.id


def do_logout():
    if CURRENT_USER_KEY in session:
        del session[CURRENT_USER_KEY]
        
        
def retrieve_users(id):
    user = User.query.get_or_404(id)
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return user, this_user


@app.route('/')
def homepage():
    this_user = None
    
    if CURRENT_USER_KEY in session:
        this_user = User.query.get_or_404(session[CURRENT_USER_KEY])

    return render_template('homepage.html', this_user=this_user)


@app.route('/signup', methods=['GET'])
def get_signup_form():
    form = NewUserForm()
    return render_template('/signup_and_login/signup.html', form=form)


@app.route('/signup', methods=['POST'])
def user_signup():
    form = NewUserForm()
    this_user = validate_and_signup(form)
    
    if not this_user:
        flash('Username already taken', 'danger')
        return render_template('/signup_and_login/signup.html', form=form)
        
    do_login(this_user)
    flash(f"Welcome to MovieBuddy, {this_user.username}", 'success')
    
    return redirect(f"/users/{this_user.id}")


@app.route('/login', methods=['GET'])
def get_login_form():
    form = UserLoginForm()
    return render_template('/signup_and_login/login.html', form=form) 
    

@app.route('/login', methods=['POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = authenticate( form.username.data, form.password.data)
        
        if user:
            do_login(user)
            flash(f"Welcome back {user.username}", 'success')
            return redirect(f"/users/{user.id}")
        
        flash('Invalid credentials. Please try again.', 'danger')
    
    return redirect('/login')


@app.route('/logout')
def logout():
    do_logout()
    
    return redirect('/')


@app.route('/get-movie-by-query', methods=['GET'])
def get_move_by_query():
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    title = request.args.get('q')
    res = requests.get(f"http://127.0.0.1:5000/api/get-movie-details/base/{title}")
    res = json.loads(res.text)['results']

    return render_template('search/show-query-results.html', res=res, query=title, this_user=this_user)


@app.route('/show-movie-details/<string:imDb_id>')
def show_movie_details(imDb_id):
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    movie_details = retrieve_movie_details(imDb_id)
    
    return render_template('show-movie-details.html',
                           imDb_id=imDb_id, 
                           title=movie_details['title'], 
                           directors=movie_details['directors'], 
                           writers=movie_details['writers'],
                           actors=movie_details['actors'],
                           plot=movie_details['plot'],
                           poster=movie_details['poster'],
                           ratings =movie_details['ratings'],
                           this_user=this_user)


@app.route('/users/<int:id>')
def show_user_profile(id):
    user, this_user = retrieve_users(id)
    return render_template('user/show_profile_details.html', user=user, this_user=this_user)

@app.route('/users/find')
def find_new_friends():
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    user = this_user
    search = request.args.get('friend-query')
    users = User.query.filter(User.username.like(f"%{search}%")).all() if search else User.query.all() 

    return render_template('user/index.html', users=users, user=user, this_user=this_user, is_following=is_following)

@app.route('/users/<int:id>/show-lists', methods=['GET'])
def show_user_lists(id):
    user, this_user = retrieve_users(id)
    return render_template('user/show_user_lists.html', user=user, this_user=this_user)


@app.route('/users/<int:id>/following', methods=['GET'])
def show_user_following(id):
    user, this_user = retrieve_users(id)
    return render_template('user/following.html', user=user, this_user=this_user, is_following=is_following)


@app.route('/users/<int:id>/followers', methods=['GET'])
def show_user_followers(id):
    user, this_user = retrieve_users(id)
    return render_template('user/followers.html', user=user, this_user=this_user, is_following=is_following)


@app.route('/users/new-list', methods=['GET']) 
def get_new_list_form():
    form = NewListForm()
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    return render_template('lists/new_movie_list_form.html', this_user=this_user, form=form, new=True)
    

@app.route('/users/new-list', methods=['POST'])
def make_new_movie_list():
    form = NewListForm()
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    new_list = validate_and_create_movie_list(form, this_user)
    
    if not new_list:
        flash('Invalid', 'danger')
        return redirect('users/new-list')
        
    flash(f"{new_list.title} successfully created", 'success')
    return redirect(f"/users/{this_user.id}/show-lists")


@app.route('/users/<int:id>/edit-profile', methods=['GET'])
def get_edit_profile_form(id):
    form = EditUserForm()
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    pre_populate_user_edit_form_fields(form, this_user)
    
    return render_template('user/edit_profile.html', this_user=this_user, form=form)
    

@app.route('/users/<int:id>/edit-profile', methods=['POST'])
def edit_user_profile(id):
    form = EditUserForm()
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    if validate_and_edit_profile(form, this_user):
        flash('Your account has been updated.', 'success')
    else:
        flash('Incorrect password.', 'danger')
        
    return redirect(f"/users/{this_user.id}")


@app.route('/users/delete', methods=['GET', 'DELETE'])
def delete_user():
    user = User.query.get_or_404(session[CURRENT_USER_KEY])
    do_logout()

    db.session.delete(user)
    db.session.commit()
    flash('We will miss you!', 'success')
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


@app.route('/users/<int:user_id>/lists/<int:list_id>/details', methods=['GET'])
def show_user_list_details(user_id, list_id):
    user, this_user = retrieve_users(user_id)
    movie_list = MovieList.query.get_or_404(list_id)
    return render_template('lists/show_user_list.html', user=user,this_user=this_user,movie_list=movie_list)
    
    
@app.route('/users/lists/<int:movie_list_id>/delete', methods=['GET', 'DELETE'])
def delete_movie_list(movie_list_id):
    movie_list = MovieList.query.get_or_404(movie_list_id)
    user_id = movie_list.owner
    
    db.session.delete(movie_list)
    db.session.commit()
    
    return redirect(f"/users/{user_id}")


@app.route('/users/lists/<int:list_id>/edit', methods=['GET', 'POST']) # PUT/PATCH wont work here. Why?
def edit_user_list(list_id):
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    movie_list = MovieList.query.get_or_404(list_id)
    form = EditListForm()
    
    if form.validate_on_submit():
        prepopulate_edit_list_form(movie_list, form)
        db.session.add(movie_list)
        db.session.commit()
        return redirect(f"/users/{this_user.id}/show-lists")
        
    update_movie_list_data(form, movie_list)

    return render_template('lists/new_movie_list_form.html', this_user=this_user, form=form, new=False)


@app.route('/users/lists/<int:movie_list_id>/add-movie/<string:imDb_id>', methods=['GET', 'POST'])
def add_movie_to_list_form(movie_list_id, imDb_id):
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    add_movie_to_list(movie_list_id, imDb_id, this_user)
    
    return redirect(f"/users/{this_user.id}/lists/{movie_list_id}/details")


@app.route('/users/lists/movies/<int:movie_id>/remove', methods=['GET', 'DELETE'])
def remove_movie_from_list(movie_id):
    this_user = User.query.get_or_404(session[CURRENT_USER_KEY])
    movie = Movie.query.get_or_404(movie_id)
   
    db.session.delete(movie)
    db.session.commit()
    
    return redirect(f"/users/{this_user.id}/show-lists")

@app.route('/api/new-comment', methods=['POST'])
def add_new_comment_to_movie_list():
    user_id = request.json['userID']
    list_id = request.json['listID']
    content = request.json['content']

    new_comment = Comment(user_id=user_id, list_id=list_id, content=content)

    db.session.add(new_comment)
    db.session.commit()
    
    return (jsonify(True), 201)

@app.route('/api/get-movie-details/<string:type>/<string:query>', methods=['GET'])
def get_movie_details(query, type):
    '''External API calls'''
    res = requests.get(f"{URL_DICTIONARY[type]}/{query}").text
    return jsonify(json.loads(res))
