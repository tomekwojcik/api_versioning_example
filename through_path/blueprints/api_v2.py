# -*- coding: utf-8 -*-

from flask import Blueprint

api_v2_blueprint = Blueprint('api_v2', __name__, url_prefix='/api/v2')


@api_v2_blueprint.route('/')
def get_api_v2_index():
    return 'Hello, APIv2!'
