import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db_drop_and_create_all


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db_drop_and_create_all()  # Should be uncommeted if we want to drop and re-create the db
    CORS(app) # this will allow all origins and headers to access the API
    # use the below CORS intialization format to allow certain headers/origins
    #  example: CORS(app, allow_headers=["header_1", "header_2"], resources={
    #    r"*": {"origins": ["origin_1", "origin_2"]}})

    return app


app = create_app()


@app.route('/', methods=['POST', 'GET'])
def health():
    return jsonify("Healthy")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
