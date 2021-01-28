import random
from utility_functions import URL_DICTIONARY
import requests
import json


class UserMovieRecommendations():
    
    def __init__(self, actors):
        self.actors = actors
        self.random_actors = []
        self.suggested_movie_ids = []

    def random_actors_select(self, num_samples):
        """Returns num_samples of actor objects from the list of self.actors"""
        
        num_samples = num_samples if num_samples < len(self.actors) else len(self.actors)
        self.random_actors = random.sample(self.actors, num_samples)

    def retrieve_list_of_imdb_movie_ids_based_on_actor(self, imdb_name_id):
        """Returns a list of all imdb movie ids associated with the imdb_name_id 
           (all of the movie ids from the movies that the given actor has been in)"""

        actor_name_res = requests.get(f"{URL_DICTIONARY['actors']}/{imdb_name_id}").text 
        actor_name_res = json.loads(actor_name_res)

        list_of_imdb_movie_ids = [movie_obj['id'] for movie_obj in actor_name_res['castMovies']]
        
        return list_of_imdb_movie_ids

    def collect_recommended_movie_ids(self, n_actor_ids_per_list, n_movie_recommendations_ids):
        """Collects n_movie_recommendation ids for every actor id in actor_list"""
        
        self.random_actors_select(n_actor_ids_per_list)

        for actor_object in self.random_actors:
            movie_ids = self.retrieve_list_of_imdb_movie_ids_based_on_actor(actor_object.imdb_id) 
            self.suggested_movie_ids.append(movie_ids[2:n_movie_recommendations_ids+2])

    def make_movie_dict(self, movie_res, wiki_res):
        plot = wiki_res['plotShort']['plainText']
        plot_text = plot if plot not in [None, ''] else movie_res['plot']
        movie = {
            'imdb_id': movie_res['id'],
            'name': movie_res['fullTitle'],
            'poster_url': movie_res['image'],
            'plot': plot_text
        }
        return movie

    def collect_recommended_movies(self, num_actors, num_movies_per_actor):
        """Collects num_actors * num_movies_per_actor recommended movies"""
        recommended_movies = []
        self.collect_recommended_movie_ids(num_actors, num_movies_per_actor)
        for movie_id_list in self.suggested_movie_ids:
            for movie_id in movie_id_list:
                wiki_res = requests.get(f"{URL_DICTIONARY['wiki']}/{movie_id}").text
                wiki_res = json.loads(wiki_res)
                movie_res = requests.get(f"{URL_DICTIONARY['movies']}/{movie_id}").text 
                movie_res = json.loads(movie_res)
                recommended_movies.append(self.make_movie_dict(movie_res, wiki_res))

        return recommended_movies
