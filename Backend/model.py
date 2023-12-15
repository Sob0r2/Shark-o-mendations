import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from Backend.reviews import Reviews


class SAE(nn.Module):
    def __init__(self, ):
        super(SAE, self).__init__()
        self.fc1 = nn.Linear(995, 80)
        self.fc2 = nn.Linear(80, 50)
        self.fc3 = nn.Linear(50, 80)
        self.fc4 = nn.Linear(80, 995)
        self.activation = nn.ReLU()
    def forward(self, x):
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.activation(self.fc3(x))
        x = F.sigmoid(self.fc4(x)) * 5
        return x

class Model:

    def __init__(self):

        self.ae = torch.load(r'C:\Users\jakub\Projekt\Model Deployment\model',map_location=torch.device('cpu'))
        self.ae.eval()
        self.res = {}
        self.movies = pd.read_csv(r"C:\Users\jakub\Projekt\DATA\Final_movies_data.csv", encoding='ISO-8859-1')
        self.reviews = Reviews()

    def get_results(self):
        data = self.reviews.data
        user_ind = [int(k) for k,v in data.items() if v != 0]
        input = torch.Tensor(list(data.values()))
        input = Variable(input)
        with torch.no_grad():
            output = self.ae(input)
        output = ((output-min(output))/(max(output)-min(output))) * 100
        self.res = self.create_dataframe(output,user_ind)
        return self.res, self.get_genres()

    def give_arr(self,row):
        row = row.replace(']','').replace('[','').replace('\'','').replace(' ','')
        return row.split(',')

    def get_genres(self):
        self.res['genres'] = self.res['genres'].apply(self.give_arr)
        df_exploded  = self.res.explode('genres')
        return df_exploded ['genres'].unique()[(df_exploded['genres'].unique() != '(nogenreslisted)') &
                                                         (df_exploded['genres'].unique() != 'IMAX')]

    def create_dataframe(self,output,user_ind):

        res = {k: round(float(v.detach()), 2) for k, v in enumerate(output)}
        res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
        res = dict(filter(lambda x: x[0] not in user_ind, res.items()))

        res = self.to_dataframe(res)

        return pd.merge(self.movies,res,on='movieID',how='right')[['title','genres','data','movieID','rating']]


    def to_dataframe(self,act):
        keys_array = np.array(list(act.keys())).reshape(-1, 1)
        values_array = np.array(list(act.values())).reshape(-1, 1)

        keys_flat = keys_array.flatten()
        values_flat = values_array.flatten()

        res = pd.DataFrame({"movieID": keys_flat, "rating": values_flat})

        return res
