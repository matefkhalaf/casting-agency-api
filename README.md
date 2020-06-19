# FSND-Casting-Agency

Udacity Full Stack Nanodegree capstone project - Casting Ageny

## Motivation

This project is the capstone project for `Udacity Full Stack web development nanondegree`.

This project covers all the learnt concepts during the nanodegree which includes data modeling for web using `postgres`, API development and testing with `Flask`, Authorization with RBAC, `JWT` authentication and finally API deployment using `Heroku`.

## Start the project locally

This section will introduce you to how to run and setup the app locally.

### Dependencies

This project is based on `Python 3` and `Flask`.

To install project dependencies:

```bash
$ pip install -r requirements.txt
```

Note: you must have the latest version of Python 3

### Local Database connection

- You need to install and start `postgres` database.
- You need to update the database_params variable found in `config.py` file as shown below:

```python
database_params = {
    "username": "postgres",
    "password": "YOUR_DB_PASSWORD",
    "db_name": "casting_agency",
    "dialect": "postgresql"
}
```

Note: you can create a db named `casting_agency` by using `createdb` command as shown below:

```bash
createdb -U postgres casting_agency
```

### Auth0 configs

You need to update auth0_params variable found in `config.py` with auth0 configurations

```python
auth0_params = {

    "AUTH0_DOMAIN": "matef.auth0.com",
    "ALGORITHMS": ['RS256'],
    "API_AUDIENCE": "myapp"
}

```

### Run the app locally

You can run the app using the below commands:

```bash
export FLASK_APP=app.py
flask run
```

### Run test cases

You can run the unit test cases that are defined in `test_app.py` using the below command:

```bash
python test_app.py
```

## API Documentation

This section will introduce you to API endpoints and error handling

### Base URL:


### Error handling

Errors are returned as JSON in the following format:

```json
{
  "success": False,
  "error": 404,
  "message": "resource not found"
}
```

The API will return the types of errors:

- 400 – bad request
- 404 – resource not found
- 422 – unprocessable
- 500 - internal server error
- 401 - unauthorized

### API Endpoints

This API supports two types of resources `/actors` and `/movies`. Each resource support four HTTP methods; `GET, POST, PATCH, DELETE`

<b>Notes</b>
- <b>You need to update the ACCESS_TOKEN in the below requests with JWT valid token.</b>
- <b>The below requests assumes you are running the app locally, so you need to update the requests with the base URL or your URL after deployment.</b>

#### GET /actors

- General: returns a list of all actors
- Sample request:

```bash
curl -X GET http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"
```

- Sample response:

```json
{
  "actors": [
    { "age": 25, "gender": "Male", "id": 1, "name": "Mohamed" },
    { "age": 26, "gender": "Male", "id": 2, "name": "Khalaf" },
    { "age": 23, "gender": "Female", "id": 3, "name": "Monica" }
  ],
  "success": true
}
```

#### GET /movies

- General: returns a list of all movies
- Sample request:

```bash
curl -X GET http://127.0.0.1:5000/movies -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"
```

- Sample response:

```json
{
  "movies": [
    {
      "actors": ["Mohamed", "Khalaf"],
      "id": 1,
      "release_date": "Mon, 15 Jun 2020 00:00:00 GMT",
      "title": "Shawshank_Redemption"
    },
    {
      "actors": ["Monica"],
      "id": 2,
      "release_date": "Mon, 15 Jun 2020 00:00:00 GMT",
      "title": "Happy_Days"
    }
  ],
  "success": true
}
```

#### POST /actors

- General: create a new actor
- Sample request:

```bash
curl -X POST http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"  -d '{"name" : "New_Actor_1", "age" : "30", "gender":"Male"}'
```

- Sample response: <i>returns the new actor id</i>

```json
{ "created": 4, "success": true }
```

#### POST /movies

- General: create a new movie
- Sample request:

```bash
curl -X POST http://127.0.0.1:5000/movies -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{"title" : "New_Movie_1", "release_date" : "12/6/2020"}'
```

- Sample response: <i>returns the new movie id</i>

```json
{ "created": 3, "success": true }
```

#### PATCH /actors/\<int:actor_id\>

- General: update an existing actor
- Sample request:
  <i>you can update actor's name, gender and age</i>

```bash
curl -X PATCH http://127.0.0.1:5000/actors/1 -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{"name" : "Mohamed Khalaf"}'
```

- Sample response: <i>returns the updated actor object</i>

```json
{
  "actor": { "age": 25, "gender": "Male", "id": 1, "name": "Mohamed Khalaf" },
  "success": true
}
```

#### PATCH /movies/\<int:movie_id\>

- General: update an existing movie
- Sample request:
  <i>you can update movies's title and release date</i>

```bash
curl -X PATCH http://127.0.0.1:5000/movies/1 -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{"title" : "UPDATE_NAME", "release_dat" : "12/6/2020"
}'
```

- Sample response: <i>returns the updated movie object which includes the actors acting in this movie</i>

```json
{
  "movie": {
    "actors": ["Mohamed Khalaf", "Khalaf"],
    "id": 1,
    "release_date": "Mon, 15 Jun 2020 00:00:00 GMT",
    "title": "Movie_Title"
  },
  "success": true
}
```

#### DELETE /actors/\<int:actor_id\>

- General: delete an existing actor
- Sample request:

```bash
curl -X DELETE http://127.0.0.1:5000/actors/1 -H "Authorization: Bearer ACCESS_TOKEN"
```

- Sample response: <i>returns the deleted actor id</i>

```json
{ "delete": 1, "success": true }
```

#### DELETE /movies/\<int:movie_id\>

- General: delete an existing movie
- Sample request:

```bash
curl -X DELETE http://127.0.0.1:5000/movies/1 -H "Authorization: Bearer ACCESS_TOKEN"
```

- Sample response: <i>returns the deleted movie id</i>

```json
{ "delete": 1, "success": true }
```

## Authentication and authorization

This API uses Auth0 for authentication, you will need to setup Auth0 application and API. You will need to update auth0_params variable found in config.py.

You can use the below links to setup auth0:

[Auth0 Applications](https://auth0.com/docs/applications)
<br>
[Auth0 APIs](https://auth0.com/docs/api/info)

### Existing user roles



1. Casting Assistant:

- GET /actors (get:actors): can get all actors
- GET /movies (get:movies): can get all movies

2. Casting Director:
- All permissions of `Casting Assistant`
- POST /actors (create:actors): can create new actors
- PATCH /actors (update:actors): can update existing actors
- PATCH /movies (update:movies): can update existing movies
- DELETE /actors (delete:actors): can delete actors from database

3. Exectutive Director:
- All permissions of `Casting Director`
- POST /movies (create:movies): Can create new movies
- DELETE /movies (delete:movies): Can delete movies from database
