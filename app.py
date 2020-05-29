import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db_drop_and_create_all, setup_db, Actor, Movie    #, Performance

# ROWS_PER_PAGE defines the number of objects to be returned in paginated results. 
# Hardocded here but could be changed.
ROWS_PER_PAGE = 10

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  db_drop_and_create_all() # uncomment this if you want to start a new database on app refresh

  CORS(app, resources={'/': {'origins': '*'}})
  
#-----------------------------------------
# Headers required for Authentication 
#-----------------------------------------

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

#-----------------------------------------
# Custom Functions
#-----------------------------------------
  def paginate_results(request, selection):
    '''
    Helper function to paginate results to be returned by endpoint for easier use in page display. 
    Number of results included determind by the ROWS_PER_PAGE varaible.
    If no page given then default to 1. 
    '''
    page = request.args.get('page', 1, type=int)

    start =  (page - 1) * ROWS_PER_PAGE
    end = start + ROWS_PER_PAGE

    paginated_results = [item.format() for item in selection]
    current_results = paginated_results[start:end]
    return current_results

#----------------------------------------
# API Endpoints: 8 in total 
#   Movies: GET, POST, PATCH, DELETE
#   Actors: GET, POST, PATCH, DELETE
#----------------------------------------

  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(jwt):
    ''' 
    Returns a paginated list of movies formatted based on the page requested. 
    If no movies found then "404: Not Found" error given. 
    '''
    try:
      movies = Movie.query.order_by(Movie.id).all()

      current_movies = paginate_results(request, movies)

      if len(current_movies)==0:
        abort(404)

      return jsonify({
        "success": True, 
        "movies": current_movies
      })
    except Exception: 
      abort(500)

  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(jwt): 
    ''' 
    Returns a paginated list of actors formatted based on the page requested.
    If no actors found then "404: Not Found" error given. 
    '''
    try: 
      actors = Actor.query.order_by(Actor.id).all()
      current_actors = paginate_results(request, actors)

      if len(current_actors)==0:
        abort(404)

      return jsonify({
        "success": True, 
        "actors": current_actors
      })

    except Exception: 
      abort(500)

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt, movie_id): 
    '''
    Deletes a movie based on it's id given in the request. 
    If no matching id found then "404: Not Found" error given. 
    Returns the id of movie that has been successfully deleted from database. 
    '''
    if not movie_id: 
      abort(400)

    try:
      movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
      
      if movie is None:
        abort(404)

      movie.delete() 

      return jsonify({
        "success": True, 
        "delete": movie_id
      })

    except Exception:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id): 
    '''
    Deletes an actor based on it's id given in the request. 
    If no matching id found then "404: Not Found" error given. 
    Returns the id of actor that has been successfully deleted from database. 
    '''
    if not actor_id:
      abort(400)

    try:
      actor = Actor.query.filter(Actor.id==actor_id).one_or_none()
      
      if actor is None:
        abort(404)

      actor.delete() 

      return jsonify({
        "success": True, 
        "delete": actor_id
      })

    except Exception:
      abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_new_movie(jwt):
    '''
    Inserts new movie instance based on fields given in the request. 
    If required fields are missing "400: ???" error given. 
    Returns the id of the movie sucessfully inserted. 
    '''
    new_title = request.json.get('title', None)
    new_release_date = request.json.get('release_date', None)

    if (new_title is None) or (new_release_date is None):
      abort(400)
    else:
      new_movie = Movie(title=new_title, release_date=new_release_date)
      try:
        new_movie.insert()
      except Exception:
        abort(422)

    created_movie = Movie.query.filter(Movie.title==new_title, Movie.release_date==new_release_date).one_or_none()

    if created_movie is None:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'movie_id': created_movie.id
      })

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_new_actor(jwt):
    '''
    Inserts new actor instance based on fields given in the request. 
    If required fields are missing "400: ???" error given. 
    Returns the id of the actor sucessfully inserted. 
    '''
    new_name = request.json.get('name')
    new_age = request.json.get('age')
    new_gender = request.json.get('gender')

    if (new_name is None) or (new_age is None) or (new_gender is None):
      abort(400)
    else:
      new_actor = Actor(name=new_name, age=new_age, gender=new_gender)
      try:
        new_actor.insert()
      except Exception:
        abort(422)

    created_actor = Actor.query.filter(Actor.name==new_name, Actor.age==new_age, Actor.gender==new_gender).one_or_none()

    if created_actor is None:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'actor_id': created_actor.id
      })

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def updating_movie(jwt, movie_id):
    '''
    Updated an existing movie given it's id and parameters to be updated. 
    If required fields are missing "422: ???" error given. 
    Returns the object of the movie sucessfully updated. 
    '''
    body=request.get_json()
    update_title = body.get('title')
    update_release_date = body.get('release_date')

    if ((update_title is None) and (update_release_date is None)):
      abort(422)

    movie = Movie.query.filter(Movie.id==movie_id).one_or_none()

    if movie is None: 
      abort(404)

    try: 
      if update_title:
        movie.title = update_title
      if update_release_date:
        movie.release_date= update_release_date
      
      movie.update()

      return jsonify({
        "success": True, 
        "movie_id": movie_id,
        "movie": [movie.format()]
      })

    except Exception:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def updating_actor(jwt, actor_id):
    '''
    Updated an existing actor given it's id and parameters to be updated. 
    If required fields are missing "422: ???" error given. 
    Returns the object of the actor sucessfully updated. 
    '''
    body=request.get_json()
    update_name = body.get('name')
    update_age = body.get('age')
    update_gender = body.get('gender')

    if ((update_name is None) and (update_age is None) and (update_gender is None)):
      abort(422)

    actor = Actor.query.filter(Actor.id==actor_id).one_or_none()

    if actor is None: 
      abort(404)

    try: 
      if update_name:
        actor.name = update_name
      if update_age:
        actor.age= update_age
      if update_gender:
        actor.gender = update_gender
      
      actor.update()

      return jsonify({
        "success": True, 
        "actor_id": actor_id, 
        "actor": [actor.format()]
      })

    except Exception:
      abort(422)

#-------------------------------------
# Error Handelers 
#-------------------------------------

  @app.errorhandler(422)
  def unprocessable(error):
    return (jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 
    422,
    )

  @app.errorhandler(400)
  def bad_request(error):
    return (jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
      }),
      400,
    )
    
  @app.errorhandler(404)
  def not_found(error):
    return (jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
      }),
      404,
    )

  @app.errorhandler(500)
  def internal_server_error(error):
    return (jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
      }),
      500,
    )

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
    
#---------------------------------------------------------
  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)