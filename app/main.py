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
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    user_id: int | None = None
    name: str
    age: int
    gender: str
    email: str
    password: str


# temp array to store users
my_users = [
    {
        "id": "1",
        "name": "Tim Krebs",
        "age": 16,
        "gender": "male",
        "email": "timkrebs9@gmail.com",
        "password": "123456789",
    },
    {
        "id": "2",
        "name": "John Doe",
        "age": "38",
        "gender": "male",
        "email": "johndoe@gmail.com",
        "password": "123456789",
    },
]


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


# Run with: uvicorn app.main:app --reload

#######################
# User Management #
#######################


def find_user(user_id: int) -> dict | None:
    for user in my_users:
        if user["id"] == str(user_id):
            return user
    return None


def find_index_users(user_id: int) -> int | None:
    for index, user in enumerate(my_users):
        if str(user["id"]) == str(user_id):
            return index
    return None


# Create Users (POST)
@app.post("/users", status_code=201)
async def create_user(user: User) -> dict:
    user_dict = user.dict()
    user_dict["id"] = random.randint(0, 100000)
    my_users.append(user_dict)
    return {"data": user_dict}


# Read Users (GET)
@app.get("/users", status_code=200)
async def get_user() -> dict:
    return {"data": my_users}


@app.get("/users/{user_id}", status_code=200)
async def get_user_by_id(user_id: int) -> dict:
    user = find_user(user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User not with id: {user_id} found"
        )
    return {"data": user}


# Update Users (PUT, PATCH)
@app.put("/users/{user_id}", status_code=200)
async def update_user(user_id: int, user: User) -> dict:
    index = find_index_users(user_id)
    if index is None:
        raise HTTPException(
            status_code=404, detail=f"User not with id: {user_id} found"
        )

    user_dict = user.dict()
    user_dict["id"] = user_id
    my_users[index] = user_dict
    return {"data": user_dict}


# Delete Users (DELETE)
@app.delete("/users/{user_id}", status_code=200)
async def delete_user(user_id: int) -> dict:
    index = find_index_users(user_id)
    if index is None:
        raise HTTPException(
            status_code=404, detail=f"User not with id: {user_id} found"
        )
    my_users.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # type: ignore
