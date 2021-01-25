import requests
import json
from api_key import api_key
from models import db, Movie, MovieList, User
from sqlalchemy.exc import IntegrityError
from user_functions import signup, authenticate


# Note that you are limited to 100 API calls per day...
base_url = f"https://imdb-api.com/en/API/Search/{api_key}"
cast_url = f"https://imdb-api.com/en/API/FullCast/{api_key}"
wikipedia_url = f"https://imdb-api.com/en/API/Wikipedia/{api_key}"
poster_url = f"https://imdb-api.com/en/API/Posters/{api_key}"
ratings_url = f"https://imdb-api.com/en/API/Ratings/{api_key}"

URL_DICTIONARY = {'base': base_url, 'cast': cast_url, 'wiki' : wikipedia_url, 'poster': poster_url, 'ratings': ratings_url}


def collect_ratings(ratings_response):
    ratings_dict = {}
    for key,val in ratings_response.items():
        if key not in ['imDbId', 'title', 'fullTitle', 'type', 'year', 'errorMessage']:
            ratings_dict[key] = val
    return ratings_dict


def retrieve_movie_details(imDb_id):
    res = requests.get(f"http://127.0.0.1:5000/api/get-movie-details/cast/{imDb_id}") # Only works locally
    res = json.loads(res.text)

    wiki_response = requests.get(f"http://127.0.0.1:5000/api/get-movie-details/wiki/{imDb_id}") # only works locally
    wiki_response = json.loads(wiki_response.text)
    
    poster_response = requests.get(f"http://127.0.0.1:5000/api/get-movie-details/poster/{imDb_id}")
    poster_response = json.loads(poster_response.text)
    
    ratings_response = requests.get(f"http://127.0.0.1:5000/api/get-movie-details/ratings/{imDb_id}") 
    ratings_response = json.loads(ratings_response.text)
    
    return {'imDb_id': imDb_id,
            'title': res['fullTitle'],         
            'directors':res['directors'], 
            'writers':res['writers'],
            'actors':res['actors'][:10],
            'plot':wiki_response['plotShort']['plainText'],
            'poster':poster_response['posters'][0]['link'],
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


def add_movie_to_list(movie_list_id, imDb_id):
    movie_details = retrieve_movie_details(imDb_id)
    movie_add = Movie(
        IMDB_id=imDb_id,
        list_id=movie_list_id,
        name=movie_details['title'],
        poster_url=movie_details['poster'],
        plot=movie_details['plot']
    )
    
    db.session.add(movie_add)
    db.session.commit()
    return


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
