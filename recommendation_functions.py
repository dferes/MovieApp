import random
from utility_functions import URL_DICTIONARY
import requests
import json


class UserMovieRecommendations():
    
    def __init__(self, actors):
        self.actors = actors
        self.random_actors = []

    def random_actors_select(self, num_samples):
        """Returns num_samples of actor objects from the list of self.actors"""
        
        num_samples = num_samples if num_samples < len(self.actors) else len(self.actors)
        self.random_actors = random.sample(self.actors, num_samples)

    def retrieve_list_of_imdb_movie_ids_based_on_actor(self, imdb_name_id):
        """Returns a list of all imdb movie ids associated with the imdb_name_id 
           (all of the movie ids from the movies that the given actor has been in)
        """
        actor_name_res = requests.get(f"{URL_DICTIONARY['actors']}/{imdb_name_id}").text
        actor_name_res = json.loads(actor_name_res)
        print('_________----------____________')
        print(actor_name_res)
        print('_______---------_____________')

        list_of_imdb_movie_ids = [movie_obj['id'] for movie_obj in actor_name_res['castMovies']]
        
        return list_of_imdb_movie_ids

    def collect_recommended_movie_ids(self, n_actor_ids_per_list, n_movie_recommendations_ids):
        """Collects n_movie_recommendation ids for every actor id in actor_list"""
        suggested_movie_ids = []
        self.random_actors_select(n_actor_ids_per_list)
        # print('+++++++++++++++++++')
        # print(self.random_actors)
        for actor_name_id in self.random_actors:
            movie_ids = self.retrieve_list_of_imdb_movie_ids_based_on_actor(actor_name_id) 
            suggested_movie_ids.append({ actor_name_id: random.sample(movie_ids, n_movie_recommendations_ids)} )
        print('--------------------------------')
        print(suggested_movie_ids)
        return suggested_movie_ids
        