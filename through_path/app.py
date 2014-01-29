# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)


@app.route('/')
def get_app_index():
    return 'Hello, World!'

from blueprints import api_v1_blueprint
app.register_blueprint(api_v1_blueprint)

from blueprints import api_v2_blueprint
app.register_blueprint(api_v2_blueprint)

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(port=5001)
