import csv

from pymongo import MongoClient

client = MongoClient('mongodb://mongo:27017')

docs = []

with open('solubility_product.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        compound, cations, anions, dissotiation, ksp, logpr, comment, color, link = row

        cations = [x.strip() for x in cations.split(',')]
        anions = [x.strip() for x in anions.split(',')]
        doc = {
            'name': compound,
            'ions': cations + anions,
            'cations': cations,
            'anions': anions,
            'dissotiation': dissotiation,
            'ksp': ksp,
            'comment': comment,
            'color': color,
        }
        docs.append(doc)

mongodb = client['myDatabase']
mongodb.compounds.insert_many(docs)
