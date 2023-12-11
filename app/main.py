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

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
