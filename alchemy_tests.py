from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator, List, Dict, Union, Tuple
from models.alchemy_models import Seauser
from models.pydantic_models import UserRegestrationModel, AcceptedUserRegistration
import asyncio
from contextlib import asynccontextmanager
import json
from fastapi import HTTPException
#===========JSON Data load==========================
admins = dict(json.load(open("test_data.json", "r")))["admins"]
simple_users = dict(json.load(open("test_data.json", "r")))["simple users"]
#=============Working with DB========================
engine = create_async_engine("postgresql+asyncpg://seawolve:wolve@localhost/seawolves",
    future=True, echo=False, execution_options={"isolation_level": "AUTOCOMMIT"})

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@asynccontextmanager
async def get_db() -> Generator:
    """Dependency for getting async session"""
    session: AsyncSession = async_session()
    try:
        yield session
    finally:
        await session.close()
#==========================================

#==========Realize DAL=======================
class UserDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def check_email(self, email: Seauser.email) -> Union[Tuple[str], None]:
        mail = await self.db_session.execute(select(Seauser.email).where(Seauser.email == email))
        return mail.first()

    async def create(self,
                            nick_name: Seauser.nick_name,
                            email: Seauser.email,
                            hashed_password: Seauser.hashed_password) -> Seauser:
        email_check = await self.check_email(email=email)
        if email_check is None:
            new_user = Seauser(
                               nick_name=nick_name,
                               email=email,
                               hashed_password=hashed_password)
            self.db_session.add(new_user)
            await self.db_session.flush()
            return new_user
        else:
            raise HTTPException(status_code=400, detail="Email is already in use.")

    async def update(self, user_id:str, **kwargs):
        update_date = await self.db_session.execute(update(Seauser)
                            .where(Seauser.id == user_id)
                            .values(kwargs))
        return update_date

    async def delete(self, user_id:str):
        action = await self.db_session.execute(update(Seauser)
                                       .where(Seauser.id == user_id)
                                       .values(status = "deleted")
                                       .returning(Seauser.nick_name))
        return action

#===============================================

async def test_check_user_by_email(test_mail:str = "mail@mail.ru"):
    async with get_db() as session:
        user = UserDAL(db_session=session)
        result = await user.check_email(email=test_mail)
        print(result)

async def test_create_user(nick_name: str,
                           email: str, hashed_password: str,
                           input_model: UserRegestrationModel = UserRegestrationModel,
                           output_model: AcceptedUserRegistration = AcceptedUserRegistration):
    input_data = input_model(nick_name=nick_name,
                             email=email, hashed_password=hashed_password)
    output_data = output_model()
    async with get_db() as session:
        user = UserDAL(db_session=session)
        action = await user.create(**input_data.model_dump())
        out = output_data.model_validate(action)
        print(out)

async def test_update_user_data(l_n:str):
    async with get_db() as session:
        user = UserDAL(db_session=session)
        result = await user.update(mail="pynanist@gmail.com", change_last_name= l_n)
        print(result)

"""
async def test_delete_user(user_id:str, output_model:Accept_User_Delete = Accept_User_Delete):

    async with get_db() as session:
        user = UserDAL(db_session=session)
        action = await user.delete(user_id=user_id)
        output_data = output_model(nick_name = action.first()[0])
        print(output_data)
"""

if __name__ == "__main__":
    asyncio.run(test_create_user(email="katkov@gmail.com", hashed_password="12345678",
                                 nick_name="pseudolukain"))