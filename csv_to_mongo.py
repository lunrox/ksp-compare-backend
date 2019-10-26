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
            compound, cations, anions, dissotiation, ksp, logpr, comment, color_names, color_codes, link = row
        except ValueError:
            LOG.info('troubles with the line %s', i)
            raise

        cations = [x.strip() for x in cations.split(',')]
        anions = [x.strip() for x in anions.split(',')]
        color_names = [x.strip() for x in color_names.split(',')]
        color_codes = [x.strip() for x in color_codes.split(',')]
        doc = {
            'name': compound,
            'ions': cations + anions,
            'cations': cations,
            'anions': anions,
            'dissotiation': dissotiation,
            'ksp': ksp,
            'comment': comment,
            'colors': [{'name': name, 'code': code}
                       for name, code in zip(color_names, color_codes)],
        }
        docs.append(doc)

mongodb = client['myDatabase']
mongodb.compounds.insert_many(docs)
