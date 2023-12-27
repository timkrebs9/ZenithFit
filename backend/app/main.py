import time
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError, DatabaseError
from fastapi import FastAPI, HTTPException, Response, status, Depends, Request
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from .schemas import User, UserBase
from . import crud, models, schemas

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db


@app.get("/", status_code=status.HTTP_200_OK)
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


# Run with: uvicorn backend.app.main:app --reload

#######################
# User Management #
#######################

# Create Users (POST)
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> dict:
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Read Users (GET)
@app.get("/users", status_code=status.HTTP_200_OK, response_model=list[schemas.UserBase])
def get_user(db: Session = Depends(get_db)) -> list:
    return db.query(models.User).all()


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserBase)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> dict:
   return db.query(models.User).filter(models.User.id == user_id).first()


# Update Users (PUT, PATCH)
@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)) -> dict:
    #cursor.execute(
    #    """UPDATE users SET name=%s, age=%s, gender=%s, email=%s, password=%s
    #    WHERE id=%s RETURNING * """,
    #    (
    #        user.name,
    #        user.age,
    #        user.gender,
    #        user.email,
    #        user.password,
    #        str(user_id),
    #    ),
    #)
    #updated_user = cursor.fetchone()
    #conn.commit()
    #
    #if updated_user is None:
    #    raise HTTPException(
    #        status_code=404, detail=f"User not with id: {user_id} found"
    #    )

    return {"data": "updated_user"}


# Delete Users (DELETE)
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> Response:
    #cursor.execute("""DELETE FROM users WHERE id = %s RETURNING *""", (str(user_id),))
    #deleted_user = cursor.fetchone()
    #conn.commit()
    #
    #if deleted_user is None:
    #    raise HTTPException(
    #        status_code=404, detail=f"User not with id: {user_id} found"
    #    )
    #
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # type: ignore
