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

## ORM FOR DATABASES 

1. ORM stands for object relational mapper 
2. perform database operations using code that maps to SQL 
3. no need to use raw SQL 
4. SQL can be abstracted away now 
5. SQLAlchemy is being used 

## SCHEMA MODELS 

1. Schema/pydantic models define the structure of a request and response 
2. Ensures that the user adheres to an expected format 

## SQLALCHEMY MODELS 

1. responsible for defining the columns of a table .
2. used to perform crud operations on entries within the database. 

## JWT TOKEN AUTHENTICATION 

1. client supplies the username and password to the API 
2. if the client's login information is valid, then the API responds with a JWT token and supplies it to the client.
3. this JWT token can be used by the client when the client needs to be authenticated in order to access resources that requires them to be logged in. 
4. the client supplies the token in the header of their request. 
5. the api checks whether the token is valid, and if it is then it supplies the client with the resources it requires. 

### COMPONENTS OF A JWT TOKEN

1. the token is made of three individual pieces- 
    * the header of the JWT token, which contains metadata about the token 
    * the payload, which is optional, and there should be no confidential information put into the token. 
    * the token secret 
2. the three elements are combined and then a signing algorithm is used to ensure that no one is able to tamper with the token. the signature is essentially there for data integrity 

### PURPOSE OF THE SIGNATURE 

1. the header, payload and api secret are passed through a signing algorithm in order to create a token 
2. a malicious user will not be able to tamper with the signed api because the user does not have access to the api secret which was used to generate the signature in the first place 
3. the api verifies the validity of the token by 
    * the api creates a test signature by combining the header and payload recieved from the user along with the api secret which resides in the api server. 
    * the api compares the test signature and then compares it to the signature recieved from the user 
    * if they match then the token is valid. 

## SQL RELATIONSHIPS 

1. in a traditional application we need to tie the post and the user who created the post which allows to assosciate the user and his post together. 
2. for this we specify a foreign key (user_id) into the posts table. 

## DATABASE MIGRATION TOOL 

1. a limitation of sqlalchemy is that it will only create a table if it sees that a table with the same name does not already exist  
2. if we make changes to the columns of a table or add a foreign key to it or anything, sqlalchemy will not do anything to the table because it already exists. 
3. to overcome this limitation we use different database migration tools. 
4. we use alembic for this purpose. 

### ALEMBIC 

1. allows us to incrementally track changes to the database schema and rollback changes to any point in time
