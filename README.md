# Chip_in. Udacity Capstone

#### Motivation for the Project

While many apps like freecycle exist to encourage re-use, they are more focussed
on individuals offloading unwanted products and require those in need to trawl 
through a lot of listings and make contact.

This project is a reversal that idea and an initial step an app that is more convenient 
and effective for both parties.

Community groups are able to advertise what they are looking for and when I as an individual
have items I want to keep out of landfill I can very quickly find a local group in need and 
arrange a drop off.

The work in this project is the conclusion of the Udacity Fullstack NanoDegree and
encapsulates the main concepts learnt regarding relational databases, REST Apis and
Identification and Authorization. 

#### URL location for the hosted API
Hosting is on Heroku

#### Project dependencies, local development and hosting instructions

#### Detailed instructions for scripts to set up authentication,install any project dependencies and run the development server.
##### Pre-requisites
You should have Python3 and pip installed on your machine

1. **Python 3.7** - 
Follow instructions to install the latest version of python for your platform in the
[python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
2. **Virtual Environment** - We recommend working within a virtual environment whenever 
using Python for projects. This keeps your dependencies for each project separate and 
organized. Instructions for setting up a virual environment for your platform can be 
found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
3. **PIP Dependencies** - Once your virtual environment is setup and running, install the 
required dependencies by navigating to the `/backend` directory and running:

``` bash
pip install -r requirements.txt
```
##### Key Pip Dependencies
- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. 
Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used
to handle the lightweight SQL database. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to 
handle cross-origin requests from our frontend server.

##### Database Setup
- Using Docker
A docker compose file and db-setup script has been provided and can be used if you have 
Docker installed locally. 

In your terminal navigate to the project root folder and run the command

``` bash
docker compose up -d
```
- Using Postgres
If you do not wish to use a container you should create a postgres db locally with the name
 `chipin` and update your .env file with the correct URL if needed.
```bash
createdb trivia 
```
- Populate the database
The database tables and seed data can be created with the following commands. 

```bash
flask db init
flask db migrate
flask db upgrade
flask initdb
```

##### Run the Server
To run the server, execute the following commands
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
##### Run Tests
 - tests and how they are run



#### Documentation of API behavior and RBAC controls
##### Getting started
- Base URL: This app can only be run locally, hosted at the default `http://127.0.0.1:5000`, 
which will be set as a proxy in the future frontend configuration.
- Authentication: 

##### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
  "success": false,
  "error": 405,
  "message": "Method not allowed"
}
```
The API will return the following errors 

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Unprocessable Entity

