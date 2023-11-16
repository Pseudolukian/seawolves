from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4
from db.sql_parser import sql_return_parser
from models.pydantic_models import CalendarCreate, AcceptedCalendarCreate
from models.alchemy_models import Calendar
from sqlalchemy import select, update, insert

class Calendar_DAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, user_id: UUID4, calendar_name: str):
        new_calendar = CalendarCreate(user_id=user_id, calendar_name=calendar_name)
        request = insert(Calendar).values(user_id=new_calendar.user_id, calendar_name=new_calendar.calendar_name).returning(Calendar)
        action = await self.db_session.execute(request)
        out = await sql_return_parser(sql_return=action, output_model=AcceptedCalendarCreate)
        return out

    async def create_task(self, calendar_id:UUID4, task_name:str, ):
        pass