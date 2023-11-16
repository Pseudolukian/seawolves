from fastapi import APIRouter, Depends, Response, Request
from models.pydantic_models import AcceptedUserRegistration, UserRegestrationModel, \
                                    UserDeleteModel, AcceptedUserDeleted, UserGetData, \
                                    AcceptedUserGetData, UserUpdateStatusModel, AcceptedUserUpdateStatusModel, \
                                    AcceptedUserLogin, AcceptedUserLogout, UserLogin

from controls.user.User_controls import UserControl
from controls.calendar.Calendar_controls import CalendarControl
from db.session import get_db
from db.user.User_DAL import UserDAL
from db.calendar.Calendar_DAL import Calendar_DAL
from pydantic import UUID4


user_router = APIRouter()
user_dal = UserDAL(db_session=get_db)
calendar_dal = Calendar_DAL(db_session=get_db)
user = UserControl(db_connection=get_db, user_dal=user_dal)
calendar = CalendarControl(db_connection=get_db, calendar_dal=calendar_dal)

@user_router.post("/sign-up", response_model=AcceptedUserRegistration)
async def create_user(user_reg_data: UserRegestrationModel = Depends(UserRegestrationModel)) -> AcceptedUserRegistration:
    new_user = await user.create_user(nick_name=user_reg_data.nick_name, email=user_reg_data.email, password=user_reg_data.hashed_password)
    await calendar.calendar_create(user_id=new_user['id'], calendar_name=user_reg_data.nick_name + '\'s calendar' )
    return new_user


@user_router.delete("/delete")
async def delete_user(user_id:UserDeleteModel = Depends(UserDeleteModel)) -> AcceptedUserDeleted:
    del_user = await user.delete_user(user_id=user_id.user_id)
    return del_user

@user_router.get("/info", response_model=AcceptedUserGetData)
async def get_user_data(user_id:UserGetData = Depends(UserGetData)) -> AcceptedUserGetData:
    user_info = await user.get_user(user_id=user_id.user_id)
    return user_info


@user_router.put("/change-user-status", response_model=AcceptedUserUpdateStatusModel)
async def user_change_data(user_id: UUID4, new_status: str = Depends(UserUpdateStatusModel)):
    change_status = await user.change_user_status(user_id=user_id, new_status=new_status.status.value)
    return change_status


@user_router.post("/log-in", response_model=AcceptedUserLogin)
async def login_user(email: str, password: str, req: Request, res: Response):
    log_in = await user.login_user(user_password=password, user_email=email)
    await user.set_cookie_login(request=req, response=res, cookie_options=UserLogin(), user_id=log_in)
    return log_in

@user_router.post("/log-out", response_model=AcceptedUserLogout)
async def logout_user(res: Response):
    await user.del_cookie_login(response=res, cookie_options=UserLogin())
    message = AcceptedUserLogout()
    return message
