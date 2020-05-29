import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie, Performance, db_drop_and_create_all
from sqlalchemy import desc
from datetime import date

#---------------------------------------------------------
# Create dict with Authorization key and Bearer token as values. 

casting_assistant_auth_header = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJjb1I0OWR1OWp4UG1wUjZaTldXQSJ9.eyJpc3MiOiJodHRwczovL2NtYWNyYWUuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlY2ZkNDEyN2E1YmFlMGJlZjI2MWMxNiIsImF1ZCI6Imh0dHBzOi8vMTI3LjAuMC4xL2NhcHN0b25lLWFwaSIsImlhdCI6MTU5MDc3NjU2OCwiZXhwIjoxNTkwNzgzNzY4LCJhenAiOiJIZENmeWllTFoyM1oxa3dRODdPeE9aR3NPem5QR2loYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.aA8yfwLlAF7GRtEEHTGnyNwLjS71Ocj9w8aq1z7pPz7k8shr7kevKNDjKobpwYto-WnbwdlyZCXHhO6n_GkYiWhkzc-iceSMvPHt2l37DxgCxexzHTy1_-PP95zX_5Rjhpcs4FRY2YvNCkSNN8B7pEg_AoFeRVXOmmihhftdMX_yfLveJKkaF8X5QSHptlXdV9p0xm7S7vaJkIkin2zwhmI1Y4L6LWgolxAxQ3QjrE8OR4e3vIFiADje3F091_9sqaYBEZikVE-f3rBJl8n8vNx1FiYdY2HdbS38qj9FQdErPr9StVkbVrHIUEtZH4ELw-_j-_xsed1IZeD9Hs9yHQ"
}

casting_director_auth_header = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJjb1I0OWR1OWp4UG1wUjZaTldXQSJ9.eyJpc3MiOiJodHRwczovL2NtYWNyYWUuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlY2ZkNDQzOWE1ZjkxMGMwZGIzMmU4NyIsImF1ZCI6Imh0dHBzOi8vMTI3LjAuMC4xL2NhcHN0b25lLWFwaSIsImlhdCI6MTU5MDc3NjYyNiwiZXhwIjoxNTkwNzgzODI2LCJhenAiOiJIZENmeWllTFoyM1oxa3dRODdPeE9aR3NPem5QR2loYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.UMcOdwmiX0eANLnpCwWAr1Nf0v6zIoFcawnVCGpJP9tBID21wdvdrKveo9rqj2EQr2hkKLlO7N5L6bgZEQpIKp19X-wyrk73OEWGc713CpVxOvmU4y4WpVxbu5yC2fceqAwGJ_I8fAy_F343a6bVTl2riKs--M-tI4BMdn52SdBKEU0XveBxcu0Ru5nDHivwII5eKEEDkl6KMsD9wDK7iyMcvip3rl68OqKe6tpXA-nay5bXGALVfc6E0EIeRwBn55lHpkkeJ-dCls760HUIgsscawR1HAy1CEt8mcG3DPv5HxAuas22Gql8RshoCHTfVhn8iusHRICwLkoacu-A7w"
}

executive_producer_auth_header = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJjb1I0OWR1OWp4UG1wUjZaTldXQSJ9.eyJpc3MiOiJodHRwczovL2NtYWNyYWUuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlY2ZkNDY3YWFlMWViMGJlNTE2MWI3YSIsImF1ZCI6Imh0dHBzOi8vMTI3LjAuMC4xL2NhcHN0b25lLWFwaSIsImlhdCI6MTU5MDc3NjQ4MiwiZXhwIjoxNTkwNzgzNjgyLCJhenAiOiJIZENmeWllTFoyM1oxa3dRODdPeE9aR3NPem5QR2loYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.shknwqkN2INFXRjA2kOjDbACFgsKyewfd2TAlSIGklyCmH85JFhO5PmBCxFc_Ns72XZRjd0rdLInq3qcspCvXpG3TQ30IMXcdH-7OvHcxhx4cTN3pdRkGlMZ88Hrg29Kk8BI6Q98mWVd3xVlQ4NjqvH5rrQvsKQFbSmVksnQTm14q3t8NDitVPYzKp6IqCmaOzFeWd8S9NAA9YKnlRMkRdNihXoPCEc1IA6r3ml2XhWYaI82fmgdDT0fgfGuRQ2u7TPc_Q8uffWrmcePqpWIdWTk_6Smp1qRBMOiOAAmDPsDUzi8e3ewyQRHK20TDPjvwh-IC9XTzogD0Eeu9534Yw"
}
#---------------------------------------------------------

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        db_drop_and_create_all() #Maybe the error is from database formatting or no entries?

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

#----------------------
# Test: GET /movies
#----------------------
    def test_get_movies(self):
        response = self.client().get("/movies", headers = casting_assistant_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data["movies"], list))
    
    def test_pagination(self):
        response = self.client().get("/movies", headers = casting_assistant_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["movies"]), 10)
        self.assertTrue(isinstance(data["movies"], list))

    def test_get_movies_nojwt(self):
        response = self.client().get("/movies")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)

#----------------------
# Test: GET /actors
#----------------------

    def test_get_actors(self):
        response = self.client().get("/actors", headers = casting_assistant_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data["actors"], list))
    
    def test_get_actors_nojwt(self):
        response = self.client().get("/actors", headers = casting_assistant_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)

#----------------------
# Test: POST /movies
#----------------------

    def test_post_movie(self):
        new_movie_json = {'title': 'James Bond', 'release_date': date.today()}

        response = self.client().post('/movies', json = new_movie_json, headers = executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        # self.assertEqual(data['movie'], 2) ##Check what this is actually suppose to be. 

    def test_post_movie_unauthorised(self):
        new_movie_json = {'title': 'James Bond', 'release_date': date.today()}

        response = self.client().post('/movies', json = new_movie_json, headers = casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
 
#----------------------
# Test: POST /actors
#----------------------

    def test_post_actor(self):
        new_actor_json = {'name': 'Ahmad ', 'age': 22, 'gender': 'male'}

        response = self.client().post('/actors', json = new_actor_json, headers = executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor'], 2) #Check if this is a correct assertion.

    def test_post_actor_unauthorised(self):
        new_actor_json = {'name': 'Ahmad ', 'age': 22, 'gender': 'male'}

        response = self.client().post('/actors', json = new_actor_json, headers = casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

#----------------------
# Test: DELETE /movies
#----------------------

    def test_movie_deletion(self):
        example_movie = Movie(title = "The Big Short", release_date=date.today())
        example_movie.insert()

        movie_id = example_movie.id

        response = self.client().delete(f"/movies/{movie_id}", headers=executive_producer_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(data["success"], False)
        self.assertEqual(data["delete"], movie_id)

        deleted_movie = Movie.query.get(movie_id)
        self.assertEqual(deleted_movie, None)

    def test_invavlid_movie_deletion(self):
        response = self.client().delete(f"/movies/0", headers=executive_producer_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_movie_deletion_unathorised(self):
        example_movie = Movie(title = "The Big Short", release_date=date.today())
        example_movie.insert()

        movie_id = example_movie.id

        response = self.client().delete(f"/movies/{movie_id}", headers=casting_assistant_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["success"])

        deleted_movie = Movie.query.get(movie_id)
        self.assertNotEqual(deleted_movie, None)

#----------------------
# Test: DELETE /actors
#----------------------

    def test_actor_deletion(self):
        example_actor = Movie(name="Tom", age=50, gender='male')
        example_actor.insert()

        actor_id = example_actor.id

        response = self.client().delete(f"/actors/{actor_id}", headers=executive_producer_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(data["success"], False)
        self.assertEqual(data["delete"], actor_id)

        deleted_actor = Actor.query.get(actor_id)
        self.assertEqual(deleted_actor, None)

    def test_invavlid_actor_deletion(self):
        response = self.client().delete(f"/actors/0", headers=executive_producer_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_actor_deletion_unathorised(self):
        example_actor = Movie(title = "Angela", age = 45, gender='female')
        example_actor.insert()

        actor_id = example_actor.id

        response = self.client().delete(f"/actors/{actor_id}", headers=casting_assistant_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["success"])

        deleted_actor = Actor.query.get(actor_id)
        self.assertNotEqual(deleted_actor, None)

#----------------------
# Test: PATCH /movies
#----------------------

    def test_patch_movie(self):
        update_movie_json = {'title': 'James Bond: Quantum Solace'}

        response = self.client().post('/movies/1', json = update_movie_json, headers = executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_id'], 1)
        #Should check here that the patched results/updated object returned is correct. 

    def test_patch_movie_unauthorised(self):
        update_movie_json = {'title': 'James Bond: Quantum Solace 2'}

        response = self.client().post('/movies/1', json = update_movie_json, headers = casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_patch_movie_invalid_body(self):
        update_movie_json = {}

        response = self.client().post('/movies/1', json = update_movie_json, headers = executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])

#----------------------
# Test: PATCH /actors
#----------------------

    def test_patch_actor(self):
        update_actor_json = {'name': 'Jamie'}

        response = self.client().post('/actors/1', json = update_actor_json, headers = executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], 1)
        #Should check here that the patched results/updated object returned is correct. 

    def test_patch_actor_unauthorised(self):
        update_actor_json = {'name': 'Jamie'}

        response = self.client().post('/actors/1', json = update_actor_json, headers = casting_assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_patch_actor_invalid_body(self):
        update_actor_json = {}

        response = self.client().post('/actors/1', json = update_actor_json, headers = executive_producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])
    

#----------------------
# Test: Error Scenarios
#----------------------  

    def test_500_internal_server_error(self):
        response = self.client().post(f"/movies", data=json.dumps(''), headers=executive_producer_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Internal Server Error")

    def test_404_not_found_error(self):
        response = self.client().get(f"/movies?page=0", headers=casting_director_auth_header)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

#---------------------------
# Test: Extra functionality
#---------------------------
    def test_invalid_page_selection(self):
        response = self.client().get("/movies?page=0")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Not Found")
  
    def test_movies_refresh_per_page(self):
        response_1 = self.client().get("/movies?page=1") 
        data_1 = json.loads(response_1.data.decode())
        response_2 = self.client().get("/movies?page=2")
        data_2 = json.loads(response_2.data.decode())

        self.assertNotEqual(data_1["movies"], data_2["movies"])

 # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
