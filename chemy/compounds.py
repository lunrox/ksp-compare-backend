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


def get_compounds_with_ion(ion):
    return mongo.db.compounds.find({"ions": {"$all": [ion]}})


@bp.route('/compounds/', methods=('POST',))
@bp.route('/compounds', methods=('POST',))
def search_compounds():
    data = request.get_json(force=True, silent=True)
    if data is None:
        raise InvalidUsage('Unable to parse input data')
    LOG.debug('data: %s', data)
    if not isinstance(data, list):
        raise InvalidUsage('Give me a list')

    if len(data) == 1:
        return dumps(get_compounds_with_ion(data[0]))

    result = []
    for subset_size in range(len(data), 1, -1):
        for subset in itertools.combinations(data, subset_size):
            result.extend(get_matched_compounds(subset))

    LOG.debug('result: %s', result)
    return dumps(result)


@bp.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
