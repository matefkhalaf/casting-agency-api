import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import setup_db, db_drop_and_create_all, Actor, Movie, Performance, db


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

# ROUTES

# GET /actors get actors endpoint
@app.route('/actors', methods=['GET'])
#@requires_auth('get:actors')
def retrieve_actors():
    selection = Actor.query.order_by(Actor.id).all()

    if len(selection) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'actors': [actor.format() for actor in selection]
    }), 200

# GET /movies get movies with their actors endpoint
@app.route('/movies', methods=['GET'])
#@requires_auth('get:movies')
def retrieve_movies():
    selection = Movie.query.order_by(Movie.id).all()

    if len(selection) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'movies': [movie.format() for movie in selection]
    }), 200

# POST /actors create a new actor
@app.route('/actors', methods=['POST'])
#@requires_auth('create:actors')
def create_actor():
    body = request.get_json()
    new_age = body.get('age', None)
    new_name = body.get('name', None)
    new_gender = body.get('gender', None)
    if ((new_age is None) or (new_name is None) or (new_gender is None)):
        abort(422)
    try:
        actor = Actor(name=new_name, gender=new_gender, age=new_age)
        actor.insert()

        return jsonify({
            'success': True,
            'created': actor.id
        }), 200

    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()

# POST /movies create a new movie
@app.route('/movies', methods=['POST'])
#@requires_auth('create:movies')
def create_movie():
    body = request.get_json()
    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)
    
    if ((new_title is None) or (new_release_date is None)):
        abort(422)
    try:
        movie = Movie(title=new_title, release_date=new_release_date)
        movie.insert()

        return jsonify({
            'success': True,
            'created': movie.id
        }), 200

    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()

# PATCH /actors/<id> update an actor
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
#@requires_auth('update:actors')
def update_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
        abort(404)
    body = request.get_json()
    new_age = body.get('age', None)
    new_name = body.get('name', None)
    new_gender = body.get('gender', None)

    if ((new_name is None) and (new_age is None) and (new_gender is None)):
        abort(422)
    try:
        if new_name is not None:
            actor.name = new_name
        if new_age is not None:
            actor.age = new_age
        if new_gender is not None:
            actor.gender = new_gender

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()

# PATCH /movies/<id> update a movie
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
#@requires_auth('update:movies')
def update_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
        abort(404)
    body = request.get_json()
    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    if ((new_title is None) and (new_release_date is None)):
        abort(422)
    try:
        if new_title is not None:
            movie.title = new_title
        if new_release_date is not None:
            movie.release_date = new_release_date
        

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


# Delete /actors/<id> delete an actor
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
#@requires_auth('delete:actors')
def delete_actor(actor_id):
    try:
        actor = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'delete': actor.id
        }), 200
    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()

# Delete /movies/<id> delete a movie
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
#@requires_auth('delete:movies')
def delete_movie(movie_id):
    try:
        movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'delete': movie.id
        }), 200
    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()

# Health check endpoint
@app.route('/health-check', methods=['POST', 'GET'])
def health_check():
    return jsonify("Health Check for the API")

# Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found. Resource Not found or Web page doesn't exist"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request. The request may be incorrect or corrupted"
    }), 400


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable Entity. An error occured while processing your request"
    }), 422


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error Occured"
    }), 500

# error handler for AuthError
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
