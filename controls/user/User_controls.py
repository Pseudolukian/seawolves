from db.user.User_DAL import UserDAL
from models.pydantic_models import AcceptedUserRegistration, AcceptedUserDeleted, AcceptedUserGetData, \
    AcceptedUserUpdateStatusModel, AcceptedUserLogin, UserLogin
from typing import Generator
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Request, Response
from pydantic import UUID4
from modules.S3.s3 import S3, s3_session

class UserControl:
    def __init__(self, db_connection:Generator, user_dal:UserDAL):
        self.db_connection = db_connection
        self.user_dal = user_dal

    async def check_cookie_login(self, request: Request, cookie_options: UserLogin) -> bool:
        check_cookie = request.cookies.get(str(cookie_options.cookie_name))
        return bool(check_cookie)

    async def set_cookie_login(self, response: Response, request: Request, cookie_options: UserLogin, user_id: UUID4):
        cookie_check = await self.check_cookie_login(request=request, cookie_options=cookie_options)
        if cookie_check:
            pass
        else:
            return response.set_cookie(key=cookie_options.cookie_name, value=str(user_id["id"]).replace('-', ''))

    async def del_cookie_login(self, response: Response, cookie_options: UserLogin):
        return response.delete_cookie(key=cookie_options.cookie_name)


    async def create_user(self, nick_name:str, email: str, password: str) -> AcceptedUserRegistration:
        s3_con = s3_session
        s3_work = S3(session=s3_con, s3_conf_path='./modules/S3/S3_structure.cfg')

        try:
            async with self.db_connection() as session:
                self.user_dal.db_session = session
                action = await self.user_dal.create(new_user_nick_name=nick_name, new_user_email=email, new_user_password=password)
                id = str(dict(action)['id'])
                await s3_work.create_structure(bucket_name='seausers', structure_name='sea_user', id=id)

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




