import csv

from pymongo import MongoClient

client = MongoClient('mongodb://mongo:27017')

docs = []

with open('solubility_product.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        compound, cations, anions, dissotiation, pr, logpr, comment, color, link = row
        doc = {
            'name': compound,
            'ions': cations.split(',') + anions.split(','),
            'cations': cations,
            'anions': anions,
            'dissotiation': dissotiation,
            'pr': pr,
            'comment': comment,
            'color': color,
        }
        docs.append(doc)

mongodb = client['myDatabase']
mongodb.compounds.insert_many(docs)
