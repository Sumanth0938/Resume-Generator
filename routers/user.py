from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy import func
from infra.database import SessionLocal
from starlette import status

from models.user import User
from apps.validator.user_validator import UserModel

import logging
import utilities.logger as Logger
error_logger = Logger.get_logger('error', logging.ERROR)
info_logger = Logger.get_logger('info', logging.INFO)

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[SessionLocal, Depends(get_db)]

@router.get("/get_user_by_id")
async def get_user_by_id(id: int,db: db_dependency):
    user = db.query(User).filter(User.id==id).first()
    try:
        if user:
            info_logger.info(f"successfully retrieved user  details for id{id}")
            return user
        raise HTTPException(status_code=404,detail="user not found")
    except Exception as e:
        error_logger.error(f"Error occurred while retrieving user details with user id: {id} error= {e}")
        raise HTTPException(status_code=500,detail="Internal server error")
    finally:
        db.close()


@router.post("/create_user",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, user_model:UserModel):
    # max_id = db.query(func.max(User.id)).scalar() or 0
    try:
        existing_user = db.query(User).filter(User.username==user_model.username).first()
        if existing_user:
            info_logger.info(f"successfully created  user  details for id {id}")
            return{'message':'user already existing','status_code':status.HTTP_409_CONFLICT}
            # raise HTTPException(status_code=400,detail="user already existing")
        new_user = User(**user_model.dict())
        db.add(new_user)
        db.commit()
        return {"message":'user created successfully'}
    except Exception as e:
         error_logger.error(f"Error occurred while creating user details with user id: {id} error= {e}")
         raise HTTPException(status_code=500,detail="Internal server error")
    finally:
        db.close()

@router.put("/update_user")
async def update_user(db:db_dependency, id: int, userModel:UserModel):
    db_user=db.query(User).filter(User.id==id).first()
    try:
        if db_user:
            db_user.username = userModel.username
            db_user.email = userModel.email
            db_user.first_name = userModel.first_name
            db_user.last_name = userModel.last_name
            db_user.role = userModel.role
            db_user.location = userModel.location
            db_user.country = userModel.country
            db_user.mobile_number = userModel.mobile_number
            db.add(db_user)
            db.commit()
            info_logger.info(f"successfully updated  user  details for id {id}")
            return {"message":"user updated successfully"}
        raise HTTPException(status_code=404,detail="id is not matching")
        
    except Exception as e:
        error_logger.error(f"Error occurred while updating user details with user id: {id} error= {e}")
        raise HTTPException(status_code=500,detail="Internal server error")
    finally:
        db.close()

@router.delete("/deleting/{user_id}")
async def delete_by_name(db: db_dependency,user_id:int):
    db_user=db.query(User).filter(User.id==user_id).first()
    try:
        if db_user:
            db.query(User).filter(User.id==user_id).delete()
            db.commit()
            info_logger.info(f"successfully deleted  user  details for id {id}")
            return {"message":"user details successfully deleted"}
        raise HTTPException(status_code=404,detail="user id  is not matching")
    except Exception as e:
        error_logger.error(f"Error occurred while deleting user details with user id: {id} error= {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()
