import logging

from bson.json_util import dumps
from flask import Blueprint, request
from flask_pymongo import PyMongo
from flask_cors import CORS


LOG = logging.getLogger(__name__)
bp = Blueprint('compounds', __name__)
CORS(bp)

mongo = PyMongo()


@bp.route('/compounds/', methods=('POST',))
@bp.route('/compounds', methods=('POST',))
def get_compounds():
    data = request.get_json(force=True)
    LOG.debug('data: %s', data)
    a = list(mongo.db.compounds.aggregate([
        {"$match": {"ions": {"$in": data}}},
        {"$addFields": {
            "order": {
                "$size": {
                    "$setIntersection": [data, "$ions"]
                }
            }
        }},
        {"$sort": {"order": -1}}
    ]))
    return dumps(a)


@bp.route('/new_compound/', methods=('POST',))
def add_compound():
    data = request.get_json(force=True)
    LOG.debug('data: %s', data)
    mongo.db.compounds.insert_one(data)
    return '', 201
