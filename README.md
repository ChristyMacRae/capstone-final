# Capstone Project

This Capstone project is the final project challenge in the Udacuty FSND course. The goal of this project is to combine all knwoeldge gained throughout the previous four projects, bringing the skills together to be able to complete a whole end to end application. 

It aimed to cover the following skills: 
* Coding in Python 
* Relational Database Architecture 
* Modeling Data Objects with SQLAlchemy
* Internet Protocols and Communication
* Developing a Flask API
* Authentication and Access
* Authentication with Auth0
* Authentication in Flask
* Role-Based Access Control (RBAC)
* Testing Flask Applications
* Deploying Applications

## Description 
This project is based a Casting Agency where the database contains two models Movies and Actors which can be queried using endpoints which will be specified in section API Documentation. Authorisation will be required in the form of Bearer tokens implemented through Auth0. 

## API Documentation 
There are a total of 8 endpoints that will be outlined below. Each will have specific permissions required which will also be defined. 

### Base URL 

https://capstone-christy.herokuapp.com

### List of Endpoints 
* Movies 
    - GET /movies 
    - POST /movies 
    - PATCH /movies 
    - DELETE /movies 
* Actors 
    - GET /actors 
    - POST /actors 
    - PATCH /actors 
    - DELETE /actors 

### Enpoint Documentation 

#### GET /movies 

```bash 
$ curl -X GET https://https://capstone-christy.herokuapp.com/movies
```

* Returns: a list of dictionaries of up to 10 movies, as results are paginated. 
* ```page``` parameter can be specified but if ommited will default to 1. 
* Headers: None 
* Permission: ```get:movies ```

Example Response 

```bash 
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 29 May 2020 00:00:00 GMT",
            "title": "The Great Escape"
        }
    ],
    "success": true
}
```

#### GET /actors

```bash 
$ curl -X GET https://https://capstone-christy.herokuapp.com/actors
```

* Returns: a list of dictionaries of up to 10 actors, as results are paginated. 
* ```page``` parameter can be specified but if ommited will default to 1. 
* Headers: None 
* Permission: ```get:actors ```

Example Response 

```bash 
{
    "actors": [
        {
            "age": 22,
            "gender": "Female",
            "id": 1,
            "name": "Christy"
        }
    ],
    "success": true
}
```

#### POST /movies

Adds a new movie object into the database. 

```bash 
$ curl -X POST https://https://capstone-christy.herokuapp.com/movies
```

* Returns: The id of the newly created movie object. 
* Headers: Required parameters - title (String) and release_date (date)
* Permissions: '''post:movies'''

Example Response 

```bash 
{
   "movie_id": 2,
   "success": true
}
```

#### POST /actors

Adds a new actor object into the database. 

```bash 
$ curl -X POST https://https://capstone-christy.herokuapp.com/actors
```

* Returns: The id of the newly created actor object. 
* Headers: Required parameters - name (String), age (Integer) and gender (String)
* Permissions: '''post:movies'''

Example Response 

```bash 
{
   "actor_id": 2,
   "success": true
}
```

#### DELETE /movies

Deletes a movie object from the database given a valid id. 

```bash 
$ curl -X DELETE https://https://capstone-christy.herokuapp.com/movies/<int:movie_id>
```

* Returns: The id of the deleted movie object. 
* Parameters: '''int:movie_id''' required in URL
* Headers: None
* Permissions: '''delete:movies'''

Example Response 

```bash 
{
   "movie_id": 2,
   "success": true
}
```

#### DELETE /actors

Deletes an actor object from the database given a valid id. 

```bash 
$ curl -X DELETE https://https://capstone-christy.herokuapp.com/actors/<int:actor_id>
```

* Returns: The id of the deleted actor object. 
* Parameters: '''int:actor_id''' required in URL
* Headers: None
* Permissions: '''delete:actors'''

Example Response 

```bash 
{
   "actor_id": 2,
   "success": true
}
```

#### PATCH /movies

Updates a movie object in the database. 

```bash 
$ curl -X POST https://https://capstone-christy.herokuapp.com/movies/<int:movie_id>
```

* Returns: The id of the newly created movie object. 
* Paramaters: '''<int:movie_id>''' must be supplied in URL.
* Headers: Required parameters - title (String) OR release_date (date)
* Permissions: '''patch:movies'''

Example Response 

```bash 
{
    "movie": [
        "title": "The Great Escape", 
        "id": 3, 
        "release_date": "Fri, 29 May 2020 00:00:00 GMT"
    ],
    "movie_id": 2,
    "success": true
}
```

#### PATCH /actors

Updates an actor object in the database. 

```bash 
$ curl -X POST https://https://capstone-christy.herokuapp.com/actors/<int:actor_id>
```

* Returns: The id of the newly created actor object. 
* Paramaters: '''<int:actor_id>''' must be supplied in URL.
* Headers: Required parameters - name (String) OR age (int) OR gender (String)
* Permissions: '''patch:actors'''

Example Response 

```bash 
{
    "actor": [
        "name": "Christy", 
        "id": 3, 
        "age": 22, 
        "gender": "female"
    ],
    "actor_id": 3,
    "success": true
}
```

## Authorisation 

### Roles 

#### Casting Assistant 

Has the following permissions: 
* ```get:movies```
* ```get:actors```

Bearer Token: ???

#### Casting Director 

Has the following permissions: 
* ```get:movies```
* ```get:actors```
* ```post:actors```
* ```delete:actors```
* ```patch:movies```
* ```patch:actors```

Bearer Token: ????

#### Executive Producer 

Has the following permissions: 
* ```get:movies```
* ```get:actors```
* ```post:actors```
* ```delete:actors```
* ```patch:movies```
* ```patch:actors```
* ```post:movies```
* ```delete:movies```

Bearer Token: ???
