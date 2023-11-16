from db.user.User_DAL import UserDAL
from db.calendar.Calendar_DAL import Calendar_DAL
from db.session import get_db
import asyncio
from controls.user.User_controls import UserControl
from controls.calendar.Calendar_controls import CalendarControl

user_dal = UserDAL(db_session=get_db)
user = UserControl(db_connection=get_db, user_dal=user_dal)
cal_dal = Calendar_DAL(db_session=get_db)
calendar = CalendarControl(db_connection=get_db,calendar_dal=cal_dal)
test_user_id = "4407ee94-25d8-409c-ba31-776cfcbfd044"
test_user_email = "test_mail_3@mail.com"
test_user_password = "A123B123"


if __name__ == "__main__":
    #print(asyncio.run(user.create_user(nick_name="nick", email = "mail233@gmail.com", password="12345678")))
    #print(asyncio.run(user.get_user(user_id=test_user_id, validate_model=UserGetData)))
    #print(asyncio.run(user.user_log_in(user_email=test_user_email, hashed_password=test_user_password)))
    #print(asyncio.run(user.delete_user(user_id=test_user_id)))
    print(asyncio.run(calendar.calendar_create(user_id=test_user_id, calendar_name='test_calendar')))