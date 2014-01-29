# -*- coding: utf-8 -*-

from flask import Blueprint

api_v1_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_v1_blueprint.route('/')
def get_api_v1_index():
    return 'Hello, APIv1!'
