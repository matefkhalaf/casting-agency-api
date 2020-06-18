import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, db_drop_and_create_all
from config import auth0_tokens, database_params


# Assign testing authorization headers

casting_assistant_auth_header = {
    'Authorization': "Bearer " + auth0_tokens["casting_assistant"]
}

casting_director_auth_header = {
    'Authorization': "Bearer " + auth0_tokens["casting_director"]
}

producer_auth_header = {
    'Authorization': "Bearer " + auth0_tokens["executive_producer"]
}

# database path
database_path = os.environ.get('DATABASE_URL', "{}://{}:{}@localhost:5432/{}".format(
    database_params["dialect"], database_params["username"], database_params["password"], database_params["db_name"]))


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test cases
    # test get actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # test get movies
    def test_get_movies(self):
        res = self.client().get('/movies', headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # test delete actor
    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=producer_auth_header)
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

    def test_422_delete_actor(self):
        res = self.client().delete('/actors/400', headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Unprocessable Entity. An error occured while processing your request")

    # test delete movie
    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

    def test_422_delete_movie(self):
        res = self.client().delete('/movies/400', headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Unprocessable Entity. An error occured while processing your request")

    # test create actor

    def test_create_actor(self):
        new_actor = {'name': 'New_Actor_1', 'age': '30', 'gender': 'Male'}
        res = self.client().post('/actors', json=new_actor, headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_actor(self):
        new_actor = {}
        res = self.client().post('/actors', json=new_actor, headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Unprocessable Entity. An error occured while processing your request")

    # test create movie
    def test_create_movie(self):
        new_movie = {'title': 'New_Movie_1', 'release_date': '12/6/2020'}
        res = self.client().post('/movies', json=new_movie, headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_movie(self):
        new_movie = {}
        res = self.client().post('/movies', json=new_movie, headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Unprocessable Entity. An error occured while processing your request")

    # test update actor
    def test_update_actor(self):
        update_actor = {'name': 'Mohamed Khalaf'}
        res = self.client().patch('/actors/2', json=update_actor,
                                   headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_update_actor(self):
        update_actor = {}
        res = self.client().patch('/actors/2', json=update_actor, headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Unprocessable Entity. An error occured while processing your request")

    # test update movie

    def test_update_movie(self):
        update_movie = {'title': 'UPDATE_NAME', 'release_dat': '12/6/2020'
                        }
        res = self.client().patch('/movies/2', json=update_movie,
                                   headers=producer_auth_header)
        #print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_update_movie(self):
        update_movie = {}
        res = self.client().patch('/movies/2', json=update_movie, headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Unprocessable Entity. An error occured while processing your request")

    # RBAC remaining tests
    # Casting assistant
    def test_get_actors_casting_assistant(self):
        res = self.client().get('/actors', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_update_movie_casting_assistant(self):
        update_movie = {'title': 'UPDATE_NAME', 'release_dat': '12/6/2020'
                        }
        res = self.client().patch('/movies/2', json=update_movie,
                                  headers=casting_assistant_auth_header)
        #print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Permission not found.")

    def test_create_movie_casting_assistant(self):
        new_movie = {'title': 'New_Movie_1', 'release_date': '12/6/2020'}
        res = self.client().post('/movies', json=new_movie, headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Permission not found.")

    # Casting Director
    def test_get_actors_casting_director(self):
        res = self.client().get('/actors', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_create_movie_casting_assistant(self):
        new_movie = {'title': 'New_Movie_1', 'release_date': '12/6/2020'}
        res = self.client().post('/movies', json=new_movie,
                                 headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Permission not found.")

    def test_delete_movie_casting_director(self):
        res = self.client().delete('/movies/1', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Permission not found.")

    # Executive producer RBAC tests are covered above

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
