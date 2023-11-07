from fastapi import APIRouter, Depends
from models.pydantic_models import AcceptedUserRegistration, UserRegestrationModel, \
                                    UserDeleteModel, AcceptedUserDeleted, UserGetData, \
                                    AcceptedUserGetData, UserUpdateStatusModel, AcceptedUserUpdateStatusModel, \
                                    AcceptedUserLogin

from controls.user.User_controls import UserControl
from db.session import get_db
from db.user.User_DAL import UserDAL
from pydantic import UUID4


user_router = APIRouter()
user_dal = UserDAL(db_session=get_db)
user = UserControl(db_connection=get_db, user_dal=user_dal)

@user_router.post("/sign-up", response_model=AcceptedUserRegistration)
async def create_user(user_reg_data:UserRegestrationModel = Depends(UserRegestrationModel)) -> AcceptedUserRegistration:
    new_user = await user.create_user(nick_name=user_reg_data.nick_name, email=user_reg_data.email,password=user_reg_data.hashed_password)
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
async def login_user(email: str, password: str):
    log_in = await user.login_user(user_password=password, user_email=email)
    return log_in


@user_router.post("/log-out")
async def logout_user():
    out = "This is user log-out end-point."
    return out
