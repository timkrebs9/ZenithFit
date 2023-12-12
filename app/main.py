# Steps to accmoplish_
# 1. Import FastAPI
# 2. Create an app instance
# 3. Create a route
# 4. Run the server

# Database Management
# 1. Import SQLAlchemy
# 2. Create a database instance
# 3. Create a model class
# 4. Create a schmea for the base user
# 5. Create a schema for the user class
# 6. Fetch the session to the main app

# Create Rest Endpoints
# 1. Create an Endpoint to Get Users
# 2. Create an Endpoint to Get Users by ID
# 3. Create an Endpoint to Create Users
# 4. Create an Endpoint to Add Users
# 5. Create an Endpoint to Update Users
# 6. Create an Endpoint to Delete Users

import random
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id  : Optional[int]
    name: str
    age: int
    gender: str
    email: str
    password: str


# temp array to store users
my_users = [{
    "id" : "1",
	"name": "Tim Krebs",
    "age" : 16,
    "gender": "male",
    "email" : "timkrebs9@gmail.com",
    "password" : "123456789"}, 
    {
    "id" : "2",
    "name": "John Doe",
    "age": "38",
    "gender": "male",
    "email": "johndoe@gmail.com",
    "password": "123456789"}
    ]


@app.get("/")
async def root():
    return {"message": "Hello World"}


#######################
# User Management #
#######################
#Create Users (POST)
@app.post("/users")
async def create_user(user: User):
    user_dict = user.dict()
    user_dict["id"] = random.randint(0,100000)
    my_users.append(user_dict)
    return {"data": user}

#Read Users (GET)
@app.get("/users/{id}")
async def get_userbyID(id: int):
    return {"data": my_users[id]}

@app.get("/users")
async def get_user():
    return {"data": my_users}

#Update Users (PUT, PATCH)
@app.put("/users/{id}")
async def update_user(id: int, user: User):
    return {"data": {id: user}}

#Delete Users (DELETE)
@app.delete("/users/{id}")
async def delete_user(id: int):
    return {"data": id}
