from db.calendar.Calendar_DAL import Calendar_DAL
from typing import Generator
from pydantic import UUID4

class CalendarControl:
    def __init__(self, db_connection: Generator, calendar_dal: Calendar_DAL):
        self.db_connection = db_connection
        self.calendar_dal = calendar_dal

    async def calendar_create(self, user_id: UUID4, calendar_name: str):
        async with self.db_connection() as session:
            self.calendar_dal.db_session = session
            action = await self.calendar_dal.create(user_id=user_id, calendar_name=calendar_name)
            return action