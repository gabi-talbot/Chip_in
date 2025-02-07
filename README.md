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
 Tests for each endpoint are provided in the test_app.py file
To deploy the tests, run

```bash
dropdb testchipin
createdb testchipin
python test_flaskr.py
```

#### Documentation of API behavior and RBAC controls
##### Getting started
- Base URL: This app can only be run locally, hosted at the default `http://127.0.0.1:5000`, 
which will be set as a proxy in the future frontend configuration.
- Authentication: There are 2 roles - admin and group owner. admin role contains permissions for all
endpoints, group owner cannot create or patch group details. The endpoints to return all groups
 and group by id are accessible without authentication. Authentication is handled by Auth0.

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

##### Endpoints

`GET /api/groups`

###### General
- Retrieves all groups from the database, ordered by county, then city. 
Results are paginated in groups of 5. If a request argument for page number is not included, page will start at 1.

- Returns 
  - 200, list of groups, items requested and the total number of groups if successful
  - 404 if no groups found.

###### Example

'curl http://127.0.0.1:5000/api/groups?page=1'

```json
{
  "groups": [
    {
      "address": "Guiness Trust, King's Road",
      "city": "London",
      "county": "Greater London",
      "description": "Your donations are hugely appreciated and help us fund life saving research. Please donate via the handy donation drop point in store.",
      "email": "info@bhf.org.uk",
      "items_requested": [
        {
          "date_requested": "Fri, 07 Feb 2025 10:48:23 GMT",
          "item_category": "Books",
          "item_id": 1,
          "item_name": "Fiction"
        },
        {
          "date_requested": "Fri, 07 Feb 2025 10:48:23 GMT",
          "item_category": "Books",
          "item_id": 2,
          "item_name": "Non-Fiction"
        },
        {
          "date_requested": "Fri, 07 Feb 2025 10:48:23 GMT",
          "item_category": "Clothes",
          "item_id": 3,
          "item_name": "Wooly Jumpers"
        }
      ],
      "name": "British Heart Foundation",
      "postcode": "SW10 0TT"
    }
  ],
  "success": true,
  "total_groups": 1
}

```
`GET /api/groups/<int:id>`
###### General
- Retrieves the specified group and items requested by that group.

- Arguments 
  - id: Group id

- Returns: 
  - 200 and group
  - 404 if not found

##### Example

`curl http://127.0.0.1:5000/api/groups/2`

```json
{
  "group": {
    "address": "Unit 3, Burley Hill",
    "city": "Leeds",
    "county": "West Yorkshire",
    "description": "Your foodbank relies on your goodwill and support.",
    "email": "info@foodbank.or.uk",
    "items_requested": [
      {
        "date_requested": "Fri, 07 Feb 2025 10:48:23 GMT",
        "item_category": "Food",
        "item_id": 4,
        "item_name": "Tinned Fruit"
      },
      {
        "date_requested": "Fri, 07 Feb 2025 10:48:23 GMT",
        "item_category": "Food",
        "item_id": 5,
        "item_name": "UHT Milk"
      },
      {
        "date_requested": "Fri, 07 Feb 2025 10:48:23 GMT",
        "item_category": "Food",
        "item_id": 6,
        "item_name": "Dried Rice"
      }
    ],
    "name": "Trussel Trust Leeds",
    "postcode": "LS4 2PU"
  },
  "success": true
}

```

`PATCH /api/groups/<int:id>`

##### General
- Updates the email address of the specified group. Requires the email details to be 
supplied in the request body.

- Arguments 
  - jwt: JWT token must have patch:group_email permission
  - id: Group Id

- Returns: 
  - 200 and id of updated group 
  - 404 if group not found 
  - 422 if request is not valid
  
##### Example

`curl -X PATCH http://127.0.0.0.1:5000/api/groups/2 -d '{"email": "patch@patched.com"}'
-H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}"`

```json
{
  "id": 2,
  "success": true
}

```

`DELETE /api/groups/<int:id>/items/<int:item_id>`

##### General
- Deletes the specified group's requested item.

- Arguments
  - jwt: Jwt must have delete:group_items permission
  - id: Group Id
  - item_id: Item Id to be deleted from the group's requested items

- Returns: 
  - 200 OK and deleted item_id if successful
  - 404 if item id not found

##### Example

`curl -X DELETE http://127.0.0.0.1:5000/api/groups/2/items/4
-H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}"`

```json
{
  "deleted_item": 4,
  "success": true
}

```

`POST /api/groups`

##### General
  
- Create a new group. Requires Group data in the request body.

- Arguments
  - jwt: Must have post:group permissions.

- Returns
  - 201 if created 
  - 422 if request body cannot be processed
  - 400 if request is in any other way invalid

##### Example

`curl -X POST http://127.0.0.0.1:5000/api/groups -d '{"name": "New Group", 
"description": "A new community group", "address": "5 New Lane", "city", "Leeds", 
"county": "Yorkshire", "postcode": "LS1 3QQ", "email": "new@group.org.uk"}'
-H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}"`

```json
{
  "success": true
}

```

`POST /api/groups/<int:id>/items`

##### General

- Adds an item to the specified group. Requires the item id in the request body.

- Arguments
  - jwt: Jwt must have post:group_items permission.
  - id: Group Id

- Returns:
  - 201 and item_id
  - 404 if item not found
  - 400 if request is not valid

##### Example

`curl -X POST http://127.0.0.1:5000/api/groups/1/items -d '{"item_id": 4}' 
-H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}"`

```json
{
  "group_id": 1,
  "success": true
}

```