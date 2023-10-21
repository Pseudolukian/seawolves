from db.user.User_DAL import UserDAL
from sqlalchemy.exc import DBAPIError
from models.alchemy_models import Seauser
from models.pydantic_models import UserRegestrationModel, UserDeleteModel, UserGetData, AcceptedUserGetData
from typing import Generator
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class UserControl:
    def __init__(self, db_connection:Generator, user_dal:UserDAL):
        self.db_connection = db_connection
        self.user_dal = user_dal

    async def create_user(self, nick_name:Seauser.nick_name,
                                  email: Seauser.email, hashed_password: Seauser.hashed_password,
                                  input_model: UserRegestrationModel = UserRegestrationModel) -> Seauser:
        input_data = input_model(nick_name=nick_name, email=email, hashed_password=hashed_password)

        async with self.db_connection() as session:
            self.user_dal.db_session = session
            try:
                action = await self.user_dal.create(**input_data.model_dump())
                return action
            except IntegrityError as e:
                if "duplicate key value violates unique constraint" in str(e):
                    raise HTTPException(status_code=400, detail="User with this email already exists.")
                else:
                    raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    async def delete_user(self, user_id:str, input_model:UserDeleteModel = UserDeleteModel) -> Seauser:
        input_model = input_model(user_id=user_id)
        async with self.db_connection() as session:
            try:
                self.user_dal.db_session = session
                action = await self.user_dal.delete(**input_model.model_dump())
                return action
            except DBAPIError as e:
                if "invalid" in str(e.orig) and "UUID" in str(e.orig):
                    raise HTTPException(status_code=400, detail=f"Invalid UUID format for user_id: {user_id}") from e
            except TypeError as e:
                raise HTTPException(status_code=400, detail=f"You input wrong user_id:{user_id}.") from e

    async def get_user(self, user_id:str, input_model:UserGetData = UserGetData) -> Seauser:
        input_model = input_model(user_id=user_id)
        async with self.db_connection() as session:

            self.user_dal.db_session = session
            action = await self.user_dal.get_user_data(**input_model.model_dump())
            return action

