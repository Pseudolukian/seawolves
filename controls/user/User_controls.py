from db.user.User_DAL import UserDAL
from sqlalchemy.exc import DBAPIError
from models.alchemy_models import Seauser
from models.pydantic_models import UserRegestrationModel, UserDeleteModel, UserGetData, UserLogin, AcceptedUserDeleted
from typing import Generator
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from pydantic import UUID4

class UserControl:
    def __init__(self, db_connection:Generator, user_dal:UserDAL):
        self.db_connection = db_connection
        self.user_dal = user_dal

    async def create_user(self, nick_name:str, email: str, password: str) -> Seauser:

        async with self.db_connection() as session:
            try:
                self.user_dal.db_session = session
                action = await self.user_dal.create(nick_name=nick_name, email=email, password=password)
                return action
            
            except IntegrityError as e:
                if "duplicate key value violates unique constraint" in str(e):
                    raise HTTPException(status_code=400, detail="User with this email already exists.")
                else:
                    raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    async def delete_user(self, user_id: UUID4) -> AcceptedUserDeleted:

        async with self.db_connection() as session:
            self.user_dal.db_session = session
            action = await self.user_dal.delete(user_id=user_id)
            if action is None:
                raise HTTPException(status_code=400, detail=f"You input wrong user_id:{user_id}.")
            else:
                return action

    async def get_user(self, user_id: UUID4, validate_model: UserGetData = UserGetData) -> Seauser:
        input_model = validate_model(user_id=user_id)

        async with self.db_connection() as session:
            self.user_dal.db_session = session
            try:
                action = await self.user_dal.get_user_data(**input_model.model_dump())
                return action
            except TypeError as e:
                raise HTTPException(status_code=400, detail=f"You input wrong user_id:{user_id}.") from e

    async def user_log_in(self, user_email:Seauser.email, hashed_password: Seauser.hashed_password, validate_model: UserLogin = UserLogin) -> Seauser:
        input_model = validate_model(user_email = user_email, hashed_password = hashed_password)

        async with self.db_connection() as session:
            self.user_dal.db_session = session
            action = await self.user_dal.user_log_in(**input_model.model_dump())
            return action



