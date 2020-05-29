from sqlalchemy import Column, String, Integer, create_engine, Date, Float
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json
from flask_migrate import Migrate

# database_path = os.environ['DATABASE_URL']
database_path = 'postgres://postgres@localhost:5432/capstone'
# database_path = 'postgres://txoytuiksvhssc:a7d9ca8df13af8faec463783b2c0cc3506b6ff348f6d2afec54af9a212abc09b@ec2-35-174-88-65.compute-1.amazonaws.com:5432/d4a91cto59cs85'

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

#----------------------------------------
# Helper methods made for initialisation
#----------------------------------------
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    new_actor = (Actor(
        name = 'Christy',
        age = 22,
        gender = 'Female'
        ))

    new_movie = (Movie(
        title = 'The Great Escape',
        release_date = date.today()
        ))

    new_performance = Performance.insert().values(
        Movie_id = new_movie.id,
        Actor_id = new_actor.id,
        actor_fee = 50.00
    )

    new_actor.insert()
    new_movie.insert()
    db.session.execute(new_performance) 
    db.session.commit()

# An association table. Possibly needs more work still need to verify working correctly. 
Performance = db.Table('Performance', db.Model.metadata,
    db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('Actor_id', db.Integer, db.ForeignKey('actors.id')),
    db.Column('actor_fee', db.Float)
)

#------------
# Models
#------------

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = db.Column(Date)
    actors = db.relationship('Actor', secondary=Performance, backref=db.backref('performances', lazy='joined'))

    def __repr__(self):
        return f'<Movie {self.id}:{self.title} @{self.start_time}>'

    def init(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id, 
            'title': self.title, 
            'release_date': self.release_date
        }

class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __repr__(self):
        return f'<Actor {self.id}:{self.name}'

    def init(self, name, age, gender):
        self.name = name
        self.age = age 
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'name': self.name, 
            'age': self.age, 
            'gender': self.gender
        }
