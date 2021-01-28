from config import URL_DICTIONARY
import requests
import json
from models import db, Movie, MovieList, User, Actor
from sqlalchemy.exc import IntegrityError
from user_functions import signup, authenticate


def collect_ratings(ratings_response):
    ratings_dict = {}
    for key,val in ratings_response.items():
        if key not in ['imDbId', 'title', 'fullTitle', 'type', 'year', 'errorMessage']:
            ratings_dict[key] = val
    return ratings_dict


def retrieve_movie_details(imDb_id):
    res = requests.get(f"{URL_DICTIONARY['local']}/cast/{imDb_id}")
    res = json.loads(res.text)

    wiki_response = requests.get(f"{URL_DICTIONARY['local']}/wiki/{imDb_id}")
    wiki_response = json.loads(wiki_response.text)
    
    ratings_response = requests.get(f"{URL_DICTIONARY['local']}/ratings/{imDb_id}") 
    ratings_response = json.loads(ratings_response.text)
    
    movie_res = requests.get(f"{URL_DICTIONARY['local']}/movies/{imDb_id}")
    movie_res = json.loads(movie_res.text)
    
    plot = wiki_response['plotShort']['plainText']
    plot_text = plot if plot not in [None, ''] else movie_res['plot']

    return {'imDb_id': imDb_id,
            'title': res['fullTitle'],         
            'directors':res['directors'], 
            'writers':res['writers'],
            'actors':res['actors'][:12],
            'plot':plot_text,
            'poster':movie_res['image'],
            'ratings':collect_ratings(ratings_response)
            }
    
    
def update_user_data(form, user):
    user.bio = form.bio.data if form.bio.data else user.bio
    user.header_image_url = form.header_image_url.data if form.header_image_url.data else user.header_image_url
    user.username = form.username.data if form.username.data else user.username
    user.email = form.email.data if form.email.data else user.email
    user.user_pic_url = form.user_pic_url.data if form.user_pic_url.data else user.user_pic_url
    
    
def update_movie_list_data(form, movie_list):
    form.title.data = movie_list.title
    form.description.data = movie_list.description
    form.list_image_url = movie_list.list_image_url
    return
    

def pre_populate_user_edit_form_fields(form, user):
    form.username.data = user.username
    form.email.data = user.email
    form.user_pic_url.data = user.user_pic_url if user.user_pic_url != user.user_pic_url[0:7] != '/static' else None 
    form.bio.data = user.bio if user.bio else None


def prepopulate_edit_list_form(movie_list, form):
    movie_list.title = form.title.data if form.title.data else movie_list.title
    movie_list.description = form.description.data if form.description.data else movie_list.description
    movie_list.list_image_url = form.list_image_url.data if form.list_image_url.data else movie_list.list_image_url


def add_movie_to_list(movie_list_id, imDb_id, user_id):
    movie_details = retrieve_movie_details(imDb_id)
    movie_add = Movie(
        IMDB_id=imDb_id,
        list_id=movie_list_id,
        name=movie_details['title'],
        poster_url=movie_details['poster'],
        plot=movie_details['plot']
    )

    add_actors_to_user(movie_details['actors'], user_id)
    
    db.session.add(movie_add)
    db.session.commit()
    return

def add_actors_to_user(movie_response_actors, user):
    for actor_dict in movie_response_actors:
        if not is_duplicate_actor_name(actor_dict['name'], user.actors):
            db.session.add(
                Actor(
                    user_id=user.id,
                    imdb_id=actor_dict['id'],
                    name=actor_dict['name']
                )
            )
    db.session.commit()
    return

def is_duplicate_actor_name(name, actors):
    for actor in actors:
        if name == actor.name:
            return True
    return False

def validate_and_signup(form):
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
            return None
        
        return this_user
    
    return None


def validate_and_create_movie_list(form, this_user):
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
            return None
        
        return new_list
    
    return None


def validate_and_edit_profile(form, this_user):
    if form.validate_on_submit():
        update_user_data(form, this_user) 
        
        if authenticate(this_user.username, form.password.data):        
            db.session.add(this_user)
            db.session.commit()
            
            return True
    
    return False
