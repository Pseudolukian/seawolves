from typing import Generator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

##############################################
# BLOCK FOR COMMON INTERACTION WITH DATABASE #
##############################################

# create async engine for interaction with database
engine = create_async_engine("postgresql+asyncpg://seawolve:wolve@localhost/seawolves",
    future=True,
    echo=False,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

# create session for the interaction with database
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@asynccontextmanager
async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()