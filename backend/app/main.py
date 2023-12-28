from fastapi import FastAPI, HTTPException, Response, status, Depends, Request
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
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
def get_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list:
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserBase)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> dict:
   return db.query(models.User).filter(models.User.user_id == user_id).first()


# Update Users (PUT, PATCH)
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.update_user(db=db, user_id=user_id, user=user)



# Delete Users (DELETE)
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> Response:
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id=user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)  # type: ignore
