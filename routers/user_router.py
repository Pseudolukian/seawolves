from fastapi import APIRouter
from models.pydantic_models import Accept_Registration_User
from controllers.user.create_user import create_user

router = APIRouter()


@router.post("/sign-up", response_model=Accept_Registration_User)
async def create_user(first_name, last_name, email) -> Accept_Registration_User:
    user = await create_user(first_name=first_name, last_name=last_name, email=email)
    return user


@router.post("/delete")
async def delete_user() -> str:
    out = "This is user delete end-point."
    return out


@router.post("/change-data")
async def user_change_data():
    out = "This is user change data end-point."
    return out


@router.post("/log-in")
async def login_user():
    out = "This is user log-in end-point."
    return out


@router.post("/log-out")
async def logout_user():
    out = "This is user log-out end-point."
    return out
