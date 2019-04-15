import itertools
import logging

from bson.json_util import dumps
from flask import Blueprint, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

from chemy.exceptions import InvalidUsage

LOG = logging.getLogger(__name__)
bp = Blueprint('compounds', __name__)
CORS(bp)

mongo = PyMongo()


def get_matched_compounds(ions):
    return mongo.db.compounds.find({"ions": {"$size": len(ions), "$all": ions}})


@bp.route('/compounds/', methods=('POST',))
@bp.route('/compounds', methods=('POST',))
def get_compounds():
    data = request.get_json(force=True)
    LOG.debug('data: %s', data)
    if not isinstance(data, list):
        raise InvalidUsage('Give me a list')

    result = []
    for l in range(len(data), 1, -1):
        for subset in itertools.combinations(data, l):
            result.extend(get_matched_compounds(subset))

    LOG.debug('result: %s', result)
    return dumps(result)


@bp.route('/new_compound/', methods=('POST',))
def add_compound():
    data = request.get_json(force=True)
    LOG.debug('data: %s', data)
    mongo.db.compounds.insert_one(data)
    return '', 201


@bp.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
