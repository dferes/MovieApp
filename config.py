api_key = 'k_jg1h63to'
key = 'super_secret_key_42'

# Note that you are limited to 100 API calls per day...
base_url = f"https://imdb-api.com/en/API/Search/{api_key}"
cast_url = f"https://imdb-api.com/en/API/FullCast/{api_key}"
wikipedia_url = f"https://imdb-api.com/en/API/Wikipedia/{api_key}"
ratings_url = f"https://imdb-api.com/en/API/Ratings/{api_key}"
actors_url = f"https://imdb-api.com/en/API/Name/{api_key}"
movie_url = f"https://imdb-api.com/en/API/Title/{api_key}"
local_url = 'http://127.0.0.1:5000/api/get-movie-details'

URL_DICTIONARY = {
    'base': base_url, 
    'cast': cast_url, 
    'wiki' : wikipedia_url,  
    'ratings': ratings_url,
    'actors': actors_url,
    'movies': movie_url,
    'local': local_url
    }
