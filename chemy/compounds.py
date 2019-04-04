import logging

from bson.json_util import dumps
from flask import Blueprint, request
from flask_pymongo import PyMongo
from flask_cors import CORS


LOG = logging.getLogger(__name__)
bp = Blueprint('compounds', __name__)
CORS(bp)

mongo = PyMongo()


@bp.route('/compounds', methods=('POST',))
def get_compounds():
    data = request.get_json(force=True)
    LOG.debug('data: %s', data)
    a = list(mongo.db.compounds.find({'ions': {'$all': data}}))
    return dumps(a)


bp2 = Blueprint('add', __name__)


@bp2.route('/new_compound', methods=('POST',))
def add_compound():
    data = request.get_json(force=True)
    LOG.debug('data: %s', data)
    mongo.db.compounds.insert_one(data)
    return '', 201
