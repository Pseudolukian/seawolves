from db.user.User_DAL import UserDAL
from models.pydantic_models import AcceptedUserRegistration, AcceptedUserDeleted, AcceptedUserGetData, \
    AcceptedUserUpdateStatusModel, AcceptedUserLogin, UserRegestrationModel
from typing import Generator
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from pydantic import UUID4
from pydantic_core._pydantic_core import ValidationError


class UserControl:
    def __init__(self, db_connection:Generator, user_dal:UserDAL):
        self.db_connection = db_connection
        self.user_dal = user_dal

    async def create_user(self, nick_name:str, email: str, password: str) -> AcceptedUserRegistration:
        """
        Function creates new user and returns new user email and email,
        or raise exceptions 400, 500 if user try to regestratioing with used email or nick_name.

        **Params**
        - nick_name: str, default="def_nick_name", pattern="^[a-zA-Z0-9_]*$", max_length=30;
        - email: str, default="def_mail@mail.com", using EmailStr validator;
        - password: str, default="A123B123", pattern="^[a-zA-Z0-9]*$", max_length=9, min_length=8;

        **Returns**
        Model: AcceptedUserRegistration

        **Exception**:
        1. Status code 400:
            - User with this email already exists – exceptions raise when user try to registrating with used email;
            - User with this nick_name already exists – exceptions raise when user try to registrating with used nick_name;
        2. Status code 500:
            - Unexpected error occurred – exceptions raise when problem appereid in base connected.
        3.
        """

        try:
            async with self.db_connection() as session:
                new_user = UserRegestrationModel(nick_name=nick_name, email=email, hashed_password=password)
                self.user_dal.db_session = session
                action = await self.user_dal.create(new_user_nick_name=new_user.nick_name, new_user_email=new_user.email, new_user_password=new_user.hashed_password)
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
            try:
                async with self.db_connection() as session:
                    self.user_dal.db_session = session
                    action = await self.user_dal.get_user_data(user_id= user_id)
                    return action
            except TypeError as e:
                raise HTTPException(status_code=400, detail=f"You input wrong user_id:{user_id}.") from e

    async def change_user_status(self, user_id: UUID4, new_status: str) -> AcceptedUserUpdateStatusModel:
        async with self.db_connection() as session:
            self.user_dal.db_session = session
            action = await self.user_dal.user_change_status(user_id=user_id, new_status=new_status)
            return action

    async def login_user(self, user_email: str, user_password: str) -> AcceptedUserLogin:
        try:
            async with self.db_connection() as session:
                self.user_dal.db_session = session
                action = await self.user_dal.user_log_in(user_email=user_email, user_password=user_password)
                return action
        except TypeError as e:
            raise HTTPException(status_code=400, detail=f"You input wrong password or email.")




