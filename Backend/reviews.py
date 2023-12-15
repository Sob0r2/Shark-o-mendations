import json

class Reviews():

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Reviews, cls).__new__(cls)
            cls._instance.data = json.load(open(r'C:\Users\jakub\Projekt\Reviews.json'))
        return cls._instance

    def make_empty(self):
        self.data = {k: 0 for k, v in self.data.items()}
        self.save()

    def watched(self):
        return any(v >= 1 for k,v in self.data.items())

    def save(self):
        with open(r'C:\Users\jakub\Projekt\Reviews.json','w') as json_file:
            json.dump(self.data,json_file)
