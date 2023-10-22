from db.user.User_DAL import UserDAL
from db.session import get_db
from models.pydantic_models import UserDeleteModel, UserGetData
import asyncio
from controls.user.User_controls import UserControl

user_dal = UserDAL(db_session=get_db)
user = UserControl(db_connection=get_db, user_dal=user_dal)
test_user_id = "3010b267-4da4-4365-a1b9-57bfb35a9897"
test_user_email = "test_mail_3@mail.com"
test_user_password = "A123B123"


if __name__ == "__main__":
    print(asyncio.run(user.create_user(nick_name="nick", email = "mail233@gmail.com", password="12345678")))
    #print(asyncio.run(user.get_user(user_id=test_user_id, validate_model=UserGetData)))
    #print(asyncio.run(user.user_log_in(user_email=test_user_email, hashed_password=test_user_password)))
    #print(asyncio.run(user.delete_user(user_id=test_user_id)))