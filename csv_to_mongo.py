#!/usr/bin/env python
import csv
import logging

from pymongo import MongoClient

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
client = MongoClient('mongodb://mongo:27017')

docs = []

with open('solubility_product.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        try:
            compound, cations, anions, dissotiation, ksp, logpr, comment, color, link = row
        except ValueError:
            LOG.info('troubles with the line %s', i)
            raise

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
