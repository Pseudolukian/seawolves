from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator, List, Dict, Union, Tuple
from models.alchemy_models import Seauser
from models.pydantic_models import UserRegestrationModel, AcceptedUserRegistration, AcceptedUserDeleted, UserUpdateModel, UserUpdateStatusModel
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

    async def delete(self, user_id:str):
        action = await self.db_session.execute(update(Seauser)
                                       .where(Seauser.id == user_id)
                                       .values(status = "deleted")
                                       .returning(Seauser.nick_name, Seauser.status,Seauser.email))
        return action.first()

    async def create(self,
                            nick_name: Seauser.nick_name,
                            email: Seauser.email,
                            hashed_password: Seauser.hashed_password) -> Seauser:
        email_check = await self.check_email(email=email)
        if email_check is None:
            new_user = Seauser(nick_name=nick_name,email=email,
                               hashed_password=hashed_password)
            action = await self.db_session.execute(insert(Seauser).values(nick_name = new_user.nick_name,
                                                                          email = new_user.email,
                                                                          hashed_password = new_user.hashed_password)
                                                                    .returning(Seauser.nick_name, Seauser.email))

            return action.first()
        else:
            raise HTTPException(status_code=400, detail="Email is already in use.")

    async def update(self, user_id_to_update: Seauser.id = None,
                     nick_name_to_update: Seauser.nick_name = None,
                     first_name_to_update: Seauser.first_name = None,
                     last_name_to_update: Seauser.last_name = None,
                     email_to_update: Seauser.email = None,
                     hashed_pass_to_update: Seauser.hashed_password = None,
                     age_to_update: Seauser.age = None,
                     exp_to_update: Seauser.experience = None,
                     about_to_update: Seauser.about = None,
                     head_line_to_update: Seauser.head_line = None):

        values_to_update = {
            "nick_name": nick_name_to_update,
            "first_name": first_name_to_update,
            "last_name": last_name_to_update,
            "email": email_to_update,
            "hashed_password": hashed_pass_to_update,
            "age": age_to_update,
            "experience": exp_to_update,
            "about": about_to_update,
            "head_line": head_line_to_update
        }

        actual_updates = {key: value for key, value in values_to_update.items() if value is not None}

        if not actual_updates:
            raise ValueError("No values provided for update.")

        action = await self.db_session.execute(
            update(Seauser)
            .where(Seauser.id == user_id_to_update)
            .values(**actual_updates)
            .returning(*[getattr(Seauser, k) for k in actual_updates.keys()])
        )

        return actual_updates

    async def user_change_status(self, user_id:Seauser.id, new_status:Seauser.status):
        actual_status = await self.db_session.execute(select(Seauser.status).where(Seauser.id == user_id))
        new_status = UserUpdateStatusModel(status=new_status)

        if actual_status.first()[0] == new_status.status.value:
            raise HTTPException(status_code=400, detail="New and old statuses are the same.")
        else:
            update_status = await self.db_session.execute(update(Seauser)
                                                          .where(Seauser.id == user_id)
                                                          .values(status = new_status.status.value)
                                                          .returning(Seauser.status))

        return update_status.first()[0]

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


async def test_update_user_data(user_id_to_update:str, age:Seauser.age, nick_nam:Seauser.nick_name):
    async with get_db() as session:
        user = UserDAL(db_session=session)
        result = await user.update(user_id_to_update=user_id_to_update, age_to_update=age, nick_name_to_update=nick_nam)
        print(result)


async def test_delete_user(user_id_to_delete:str, output_model: AcceptedUserDeleted = AcceptedUserDeleted):

    async with get_db() as session:
        user = UserDAL(db_session=session)
        action = await user.delete(user_id=user_id_to_delete)
        print(action)

async def test_user_change_status(user_id_to_change:str, new_user_status:str):
    async with get_db() as session:
        user = UserDAL(db_session=session)
        action = await user.user_change_status(user_id=user_id_to_change, new_status=new_user_status)
        print(action)


if __name__ == "__main__":
    asyncio.run(test_user_change_status(user_id_to_change="51ce233e-3e40-42c7-91da-284ce45003d2", new_user_status="registrated"))
    #asyncio.run(test_update_user_data(user_id_to_update="51ce233e-3e40-42c7-91da-284ce45003d2", age=20, nick_nam="Pseudo"))
    #asyncio.run(test_create_user(nick_name="some_nick5", email="some@mail5.com", hashed_password="324324234"))
    #asyncio.run(test_delete_user(user_id_to_delete="5dc6279f-1f27-4d95-b502-124b0c55b70c"))