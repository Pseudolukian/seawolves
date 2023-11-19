from db.user.User_DAL import UserDAL
from models.pydantic_models import AcceptedUserRegistration, AcceptedUserDeleted, AcceptedUserGetData, \
    AcceptedUserUpdateStatusModel, AcceptedUserLogin, UserLogin
from typing import Generator
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from pydantic import UUID4

class UserControl:
    def __init__(self, db_connection:Generator, user_dal:UserDAL):
        self.db_connection = db_connection
        self.user_dal = user_dal


    async def create_user(self, nick_name:str, email: str, password: str) -> AcceptedUserRegistration:
        try:
            async with self.db_connection() as session:
                self.user_dal.db_session = session
                action = await self.user_dal.create(new_user_nick_name=nick_name, new_user_email=email, new_user_password=password)
                return action

        except IntegrityError as e:
            if f"DETAIL:  Key (email)=({email}) already exists." in str(e):
                raise HTTPException(status_code=400, detail="User with this email already exists.")
            if f"DETAIL:  Key (nick_name)=({nick_name}) already exists." in str(e):
                raise HTTPException(status_code=400, detail="User with this nick_name already exists.")
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

    async def get_user(self, user_id: UUID4) -> AcceptedUserGetData:
        async with self.db_connection() as session:
            self.user_dal.db_session = session
            action = await self.user_dal.get_user_data(user_id= user_id)
            if action is None:
                raise HTTPException(status_code=400, detail=f"You input wrong user_id:{user_id}.")
            else:
                return action

    async def change_user_status(self, user_id: UUID4, new_status: str) -> AcceptedUserUpdateStatusModel:
        async with self.db_connection() as session:
            self.user_dal.db_session = session
            action = await self.user_dal.user_change_status(user_id=user_id, new_status=new_status)
            if action is None:
                raise HTTPException(status_code=400, detail=f"You input wrong user_id:{user_id}.")
            else:
                return action

    async def login_user(self, user_email: str, user_password: str) -> AcceptedUserLogin:
        async with self.db_connection() as session:
            log_val = UserLogin(user_email=user_email, hashed_password=user_password)
            self.user_dal.db_session = session
            action = await self.user_dal.user_log_in(user_email=log_val.user_email, user_password=log_val.hashed_password)
            if action is None:
                raise HTTPException(status_code=400, detail=f"You input wrong email or password.")
            else:
                return action




