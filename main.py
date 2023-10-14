from fastapi import FastAPI, APIRouter, Depends
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from models.alchemy_models import Seauser
from models.pydantic_models import Accept_Registration_User, User_Registration

#=============Working with DB========================
engine = create_async_engine("postgresql+asyncpg://seawolve:wolve@localhost/seawolves",
    future=True, echo=True, execution_options={"isolation_level": "AUTOCOMMIT"})

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
#==========================================


#==========Realize DAL=======================
class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, first_name: str, last_name: str, nick_name: str, email: str, password: str) -> Seauser:
        new_user = Seauser()
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.nick_name = nick_name
        new_user.email = email
        new_user.hashed_password = password
        try:
            self.db_session.add(new_user)
            await self.db_session.flush()
            return new_user
        finally:
            await self.db_session.close()
#===============================================


#========Set routing=============#
user_router = APIRouter()
main_api_router = APIRouter()

@user_router.post("/sign-up", response_model=Accept_Registration_User)
async def create_user(user_reg_request: User_Registration, db: AsyncSession = Depends(get_db)) -> Accept_Registration_User:
    user_dal = UserDAL(db)
    user = await user_dal.create_user(
                                        first_name=user_reg_request.first_name,
                                        last_name=user_reg_request.last_name,
                                        email=user_reg_request.email,
                                        nick_name= user_reg_request.nick_name,
                                        password= user_reg_request.hashed_password
                                    )
    return user

app = FastAPI()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
