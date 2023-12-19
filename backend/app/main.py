import time
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError, DatabaseError
from fastapi import FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db
from . import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class User(BaseModel):
    user_id: int | None = None
    name: str
    age: int
    gender: str
    email: str
    password: str
    


# Laden der Umgebungsvariablen
load_dotenv()

# Datenbankverbindungsinformationen aus Umgebungsvariablen
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# Datenbankverbindung
while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connected to the database successfully")
        break
    except (OperationalError, DatabaseError) as db_error:
        print("Database connection failed")
        print("Error: ", db_error)
        time.sleep(5)

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


# Create Users (POST)
@app.post("/users", status_code=201)
async def create_user(user: User, db: Session = Depends(get_db)) -> dict:
    cursor.execute(
        """INSERT INTO users (name, age, gender, email, password)
       VALUES (%s, %s, %s, %s, %s) RETURNING *""",
        (user.name, user.age, user.gender, user.email, user.password),
    )
    new_user = cursor.fetchone()
    conn.commit()
    return {"data": new_user}


# Read Users (GET)
@app.get("/users", status_code=200)
async def get_user(db: Session = Depends(get_db)) -> dict:
    cursor.execute("SELECT * FROM users")
    my_users = cursor.fetchall()

    return {"data": my_users}


@app.get("/users/{user_id}", status_code=200)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> dict:
    cursor.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User not with id: {user_id} found"
        )
    return {"data": user}


# Update Users (PUT, PATCH)
@app.put("/users/{user_id}", status_code=200)
async def update_user(user_id: int, user: User, db: Session = Depends(get_db)) -> dict:
    cursor.execute(
        """UPDATE users SET name=%s, age=%s, gender=%s, email=%s, password=%s
        WHERE id=%s RETURNING * """,
        (
            user.name,
            user.age,
            user.gender,
            user.email,
            user.password,
            str(user_id),
        ),
    )
    updated_user = cursor.fetchone()
    conn.commit()

    if updated_user is None:
        raise HTTPException(
            status_code=404, detail=f"User not with id: {user_id} found"
        )

    return {"data": updated_user}


# Delete Users (DELETE)
@app.delete("/users/{user_id}", status_code=200)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> Response:
    cursor.execute("""DELETE FROM users WHERE id = %s RETURNING *""", (str(user_id),))
    deleted_user = cursor.fetchone()
    conn.commit()

    if deleted_user is None:
        raise HTTPException(
            status_code=404, detail=f"User not with id: {user_id} found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)  # type: ignore
