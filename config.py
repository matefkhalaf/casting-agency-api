# This file should be hidden, to not expose sensitive data
import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# database local conenction params
database_params = {
    "username": "postgres",
    "password": "root",
    "db_name": "casting_agency",
    "dialect": "postgres"
}

# auth0 config params

auth0_params = {

    "AUTH0_DOMAIN": "matef.auth0.com",
    "ALGORITHMS": ['RS256'],
    "API_AUDIENCE": "myapp"


}

