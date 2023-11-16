from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from models.alchemy_models import Seauser
from pydantic import UUID4
from models.pydantic_models import AcceptedUserDeleted, AcceptedUserRegistration, UserRegestrationModel, \
AcceptedUserGetData, AcceptedUserUpdateStatusModel, AcceptedUserLogin
from db.sql_parser import sql_return_parser

class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def delete(self, user_id:UUID4) -> AcceptedUserDeleted:
        request = update(Seauser).where(Seauser.id == user_id).values(status="deleted").returning(Seauser)
        action = await self.db_session.execute(request)
        out = await sql_return_parser(sql_return=action, output_model=AcceptedUserDeleted)
        return out

    async def create(self, new_user_nick_name: str, new_user_email: str, new_user_password: str) -> AcceptedUserRegistration:
        new_user = UserRegestrationModel(nick_name=new_user_nick_name, email=new_user_email, hashed_password=new_user_password)
        request = insert(Seauser).values(nick_name=new_user.nick_name, email=new_user.email, hashed_password=new_user.hashed_password).returning(Seauser)
        action = await self.db_session.execute(request)
        out = await sql_return_parser(sql_return=action, output_model=AcceptedUserRegistration)
        return out

    async def get_user_data(self, user_id: UUID4) -> AcceptedUserGetData:
        request = select(Seauser).where(Seauser.id == user_id)
        action = await self.db_session.execute(request)
        out = await sql_return_parser(sql_return=action, output_model=AcceptedUserGetData)
        return out

    async def user_change_status(self, user_id: UUID4, new_status: str) -> AcceptedUserUpdateStatusModel:
        request = update(Seauser).where(Seauser.id == user_id).values(status=new_status).returning(Seauser)
        action = await self.db_session.execute(request)
        out = await sql_return_parser(sql_return=action, output_model=AcceptedUserUpdateStatusModel)
        return out

    async def user_log_in(self, user_email: str, user_password: str) -> AcceptedUserLogin:
        request = select(Seauser).where(Seauser.email == user_email, Seauser.hashed_password == user_password)
        action = await self.db_session.execute(request)
        out = await sql_return_parser(sql_return=action, output_model=AcceptedUserLogin)
        return out
