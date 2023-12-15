import requests
import json
import pandas as pd

class RequestApi:

    @staticmethod
    def get_actors(tmdbid):
        movie_url = "https://api.themoviedb.org/3/movie/"
        credits_url = "/credits?api_key=28ddd70cdfdf142c70047926bc58191d"
        url = f"{movie_url}{tmdbid}{credits_url}"
        req = requests.get(url)
        actress = json.loads(req.content)
        credits = []
        for j, data in enumerate(actress["cast"]):
            if j >= 10:
                break
            credits.append(data["name"])
        return ", ".join(credits)

    @staticmethod
    def single_movie_search(title):
        movie_url = "https://api.themoviedb.org/3/search/movie?api_key=28ddd70cdfdf142c70047926bc58191d&query="
        movie_response = requests.get(movie_url+title)
        movie_data_dic = json.loads(movie_response.content)
        actors = RequestApi.get_actors(movie_data_dic["results"][00]["id"])
        overwiew = movie_data_dic["results"][00]["overview"]
        return actors,overwiew

    @staticmethod
    def get_genres(title):
        movies = pd.read_csv(r"C:\Users\jakub\Projekt\DATA\Final_movies_data.csv",encoding='ISO-8859-1')
        genres = ' '.join(str(movies[movies['title'] == title]['genres']).split('[')[1].split(']')[0].replace('\'','').split(' ')[:3])
        return genres

