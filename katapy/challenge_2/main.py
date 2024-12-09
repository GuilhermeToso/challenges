import kagglehub
from typing import Optional
import pandas as pd
import os
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

class DataSource:

    def __init__(self):
        self.path: Optional[str] = None

    def download(self, dataset: str = "yasserh/amazon-product-reviews-dataset"):
        # Download latest version
        self.path = kagglehub.dataset_download(dataset)

    def load(self) -> pd.DataFrame:

        files = os.listdir(self.path)
        get_csv_file = list(filter(lambda x: x.split('.')[-1]=='csv', files))
        
        return pd.read_csv(f"{self.path}\\{get_csv_file[0]}")


class Preprocess:

    def __init__(self, data: pd.DataFrame):
        self.data: Optional[pd.DataFrame] = data

    def filter_fields(self):
        columns = ['reviews.rating', 'reviews.text']

        return self.data[columns].copy()
    
    def clean(self):

        new_data = self.filter_fields()
        new_data.drop_duplicates(inplace=True)
        new_data.dropna(inplace=True)

        return new_data    

class Stats:

    def __init__(self, data: pd.DataFrame):
        self.data: Optional[pd.DataFrame] = data

    def get_total_reviews(self):

        return self.data.shape[0]

    def reviews_average(self):

        return self.data['reviews.rating'].sum()/self.data.shape[0]

    def get_words(self, top_n: int = 5):


        reviews = " ".join(self.data['reviews.text'].to_list())

        doc = nlp(reviews.lower())

        words = [token.text for token in doc if token.is_alpha and not token.is_stop]

        return Counter(words).most_common(top_n)

class Report:

    def __init__(self):
        self.datasource = DataSource()
        self.datasource.download()
        self.data = self.datasource.load()
        self.preprocess = Preprocess(self.data)
        self.data = self.preprocess.clean()
        self.stats = Stats(self.data)


    def generate(self):
        total_reviews = self.stats.get_total_reviews()
        average = self.stats.reviews_average()
        words = ", ".join([word[0] for word in self.stats.get_words()])
        print(f"""Product Reviews Report\n ---------------- \n Total: {total_reviews} \n Average: {average} \n Words: {words}""")
    

if __name__ == "__main__":

    report = Report()
    report.generate()