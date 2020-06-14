from sqlalchemy import Column, String, create_engine, Integer, Date
from flask_sqlalchemy import SQLAlchemy
from config import database_params
from datetime import date
import json
import os

# try to get heroku DATABASE_URL env variable or set default local db connection string
database_path = os.environ.get('DATABASE_URL', "{}://{}:{}@localhost:5432/{}".format(
    database_params["dialect"], database_params["username"], database_params["password"], database_params["db_name"]))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_populate_db()


'''
db_populate_db()
  populate the db with dummy data
'''


def db_populate_db():
    new_actor_1 = Actor('Mohamed', 'Male', '25')
    new_actor_2 = Actor('Khalaf', 'Male', '26')
    new_actor_3 = Actor('Monica', 'Female', '23')

    new_movie_1 = Movie('Shawshank_Redemption', date.today())
    new_movie_2 = Movie('Happy_Days', date.today())

    new_actor_1.insert()
    new_actor_2.insert()
    new_actor_3.insert()

    new_movie_1.insert()
    new_movie_2.insert()

    new_performance_1 = Performance.insert().values(
        movie_id=new_movie_1.id, actor_id=new_actor_1.id)
    new_performance_2 = Performance.insert().values(
        movie_id=new_movie_1.id, actor_id=new_actor_2.id)
    new_performance_3 = Performance.insert().values(
        movie_id=new_movie_2.id, actor_id=new_actor_3.id)

    db.session.execute(new_performance_1)
    db.session.execute(new_performance_2)
    db.session.execute(new_performance_3)
    db.session.commit()


'''
Performance
N:N relationship between movies and actors
'''
Performance = db.Table('performance', db.Model.metadata, db.Column('movie_id', db.Integer, db.ForeignKey(
    'movies.id')), db.Column('actor_id', db.Integer, db.ForeignKey('actors.id')))


'''
Movie
Have a title and release year
'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    actors = db.relationship('Actor', secondary=Performance,
                             backref=db.backref('performances', lazy='joined'))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}

    '''
  insert()
      inserts a new model into a database
  '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
  delete()
      deletes a new model into a database
      the model must exist in the database
  '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
  update()
      updates a new model into a database
      the model must exist in the database
  '''

    def update(self):
        db.session.commit()


'''
Actor
Have a name, age and gender
'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age}

    '''
  insert()
      inserts a new model into a database
  '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
  delete()
      deletes a new model into a database
      the model must exist in the database
  '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
  update()
      updates a new model into a database
      the model must exist in the database
  '''

    def update(self):
        db.session.commit()

