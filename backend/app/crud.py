from sqlalchemy.orm import Session

from . import models, schemas, utils

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate)->dict:
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not db_user:
        return None

    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int)->dict:
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user
