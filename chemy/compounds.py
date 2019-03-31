import logging

from bson.json_util import dumps
from flask import Blueprint, request
from flask_pymongo import PyMongo


LOG = logging.getLogger(__name__)
bp = Blueprint('compounds', __name__, url_prefix='/compounds')
mongo = PyMongo()


@bp.route('/', methods=('POST',))
def get_compounds():
    data = request.get_json(force=True)
    LOG.debug('data: %s', data)
    a = list(mongo.db.compounds.find({'ions': {'$all': data}}))
    return dumps(a)


@bp.route('/new_compound', methods=('POST',))
def add_compound():
    data = request.get_json(force=True)
    LOG.debug('data: %s', data)
    mongo.db.compounds.insert_one(data)
    return '', 201
