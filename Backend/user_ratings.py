import numpy as np
import pandas as pd

from Backend.reviews import Reviews


class User_Ratings:

    def __init__(self,ctr):
        super().__init__()
        self.movies = pd.read_csv(r"C:\Users\jakub\Projekt\DATA\Final_movies_data.csv",encoding='ISO-8859-1')
        self.num_of_movies = ctr
        self.choices = []
        self.act = 0
        self.reviews = Reviews()

    def create_swipe_blocks(self):
        idx_range = self.movies.shape[0]
        self.choices = np.random.choice(np.arange(idx_range), size=self.num_of_movies, replace=False)

    def title_and_photo_generator(self):
        if self.act < self.num_of_movies:
            title = self.movies.at[self.choices[self.act],'title']
            link = rf"C:\Users\jakub\Projekt\photos\{self.choices[self.act]}.jpg"
            self.act += 1
            return title,link
        else:
            return -1,""

    def rate(self,res):
        self.reviews.data[f'{self.choices[self.act-1]}'] = res

    def to_go(self):
        return f"{self.act}/{self.num_of_movies}"

    def finish_ratings(self):
        self.reviews.save()

