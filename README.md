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

## Requirements 

## Locally Running the Project 

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
$ curl -X GET https://https://capstone-christy.herokuapp.com/actors
```

* Returns: a list of dictionaries of up to 10 movies, as results are paginated. 
* ```bash page``` parameter can be specified but if ommited will default to 1. 
* Headers: None 
* Permission: ```bash get:movies ```

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

#### POST /movies

Adds a new movie object into the database. 

```bash 
$ curl -X POST https://https://capstone-christy.herokuapp.com/actors
```

* Returns: 
