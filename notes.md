# FastAPI Course 

## PATHS IN FastAPI
path operation, essentially a route
the 'get' in the decorator refers to the HTTP method
the path parameter is the endpoint for the operation

the difference between a get and a post request
is that a post request is used to 
send data to the server 
while a get request is used to retrieve 
data from the server

in a post requrst, the data is sent in the body of the request
to extract the data from the body of the request,
we can use the request parameter of the path operation
the Body class is used to declare 
the expected data type of the request body 
    
the body takes in the data coming from the post request and assigns it to the payload variable in form of a dictionary which can then be uses to access the data

## SCHEMA

why we need schema ?

the schema is used to declare the expected data type of the request body this is useful for validation and documentation purposes schema forces the client to send data in a schema we expect

schema is defined using the pydantic library

for a post request we want a title and a content

## CRUD 
CRUD is an acronym for Create, Read, Update, Delete

these are the four basic operations that can be performed on a database

the standard conventions for CRUD operations are-
1. Create - POST - /posts - @app.get('/posts') 
2. Read - GET - /posts/:id OR /posts - @app.get('/posts/{id}') OR @app.get('/posts')
3. Update - PUT/PATCH - /posts/:id - @app.put('/posts/{id}') OR @app.patch('/posts/{id}')
4. Delete - DELETE - /posts/:id - @app.delete('/posts/{id}')

## DATABASES 

PostgresSQL is a relational databse that can be used with FastAPI and implements SQL. 

* Each instance of postgres can be carved into multiple seperate databases
* Postgres requires the specification of the name of a database to make a connection, so there needs to be a database. 

### SCHEMA FOR TABLE 

* a table represents a subject or event in an application 
* a table is made of rows and columns 
* each column represents a different attribute 
* each row represents a different entry in the table

#### PRIMARY KEY 
1. used to uniquely identify each row in the table 
2. each table can only have one column as the primary key 
