from fastapi import APIRouter, Depends
from models.pydantic_models import AcceptedUserRegistration, UserRegestrationModel, \
                                    UserDeleteModel, AcceptedUserDeleted, UserGetData, \
                                    AcceptedUserGetData

from controls.user.User_controls import UserControl
from db.session import get_db
from db.user.User_DAL import UserDAL

user_router = APIRouter()
user_dal = UserDAL(db_session=get_db)
user = UserControl(db_connection=get_db, user_dal=user_dal)

@user_router.post("/sign-up", response_model=AcceptedUserRegistration)
async def create_user(user_reg_data:UserRegestrationModel = Depends(UserRegestrationModel)) -> AcceptedUserRegistration:
    new_user = await user.create_user(nick_name=user_reg_data.nick_name, email=user_reg_data.email,hashed_password=user_reg_data.hashed_password)
    return new_user


@user_router.delete("/delete")
async def delete_user(user_id:UserDeleteModel = Depends(UserDeleteModel)) -> AcceptedUserDeleted:
    del_user = await user.delete_user(user_id=user_id.user_id)
    return del_user

@user_router.get("/info", response_model=AcceptedUserGetData)
async def delete_user(user_id:UserGetData = Depends(UserGetData)) -> AcceptedUserGetData:
    user_info = await user.get_user(user_id=user_id.user_id)
    return user_info


@user_router.put("/change-data")
async def user_change_data():
    out = "This is user change data end-point."
    return out


@user_router.post("/log-in")
async def login_user():
    out = "This is user log-in end-point."
    return out


@user_router.post("/log-out")
async def logout_user():
    out = "This is user log-out end-point."
    return out
