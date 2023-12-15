import copy
import re

class Final_Results:
    result = None
    org = None
    act_genres = None
    genres = None
    tmp_genres = None

    @staticmethod
    def start(result, genres):
        Final_Results.result = copy.deepcopy(result)
        Final_Results.org = Final_Results.result
        Final_Results.act_genres = {i: 1 for i in genres}
        Final_Results.genres = genres
        Final_Results.tmp_genres = {i: 1 for i in genres}

    @staticmethod
    def click_button(checkbox):
        if Final_Results.act_genres[checkbox.id] == 0:
            Final_Results.act_genres[checkbox.id] = 1
        else:
            Final_Results.act_genres[checkbox.id] = 0

    @staticmethod
    def return_filtered():
        Final_Results.result = Final_Results.org[Final_Results.org['genres'].apply(
            lambda x: any(bool(re.search(genre, str(x))) and val == 1 for genre, val in Final_Results.act_genres.items()))]

    @staticmethod
    def on_entry():
        Final_Results.tmp_genres = copy.deepcopy(Final_Results.act_genres)

    @staticmethod
    def delete_changes():
        Final_Results.act_genres = copy.deepcopy(Final_Results.tmp_genres)

    @staticmethod
    def check_empty():
        return all(v == 0 for k, v in Final_Results.act_genres.items())

    @staticmethod
    def return_vals(i):
        Final_Results.result = Final_Results.result.reset_index(drop=True)
        return (
            Final_Results.result.at[i, 'title'],
            rf"C:\Users\jakub\Projekt\photos\{Final_Results.result.at[i, 'movieID']}.jpg",
            Final_Results.result.at[i, 'rating']
        )