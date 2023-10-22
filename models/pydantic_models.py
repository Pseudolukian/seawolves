from pydantic import BaseModel, Field, EmailStr, UUID4, Json
from typing import Union
from datetime import datetime
from typing import Optional
from enum import  Enum

#=======Input data models===========#
class UserExperience(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    position: str = ""
    responsibilities: str = ""

class UserChangeStatus(Enum):
    registrated: str = "registrated"
    banned: str = "banned"
    deleted: str = "deleted"
    stopped: str = "stopped"

class UserUpdateStatusModel(BaseModel):
    status: UserChangeStatus

class UserDeleteModel(BaseModel):
    user_id: UUID4 = "3010b267-4da4-4365-a1b9-57bfb35a9897"

class UserGetData(BaseModel):
    user_id: UUID4 = "3010b267-4da4-4365-a1b9-57bfb35a9897"

class UserUpdateModel(BaseModel):
    nick_name: str = Field(default="def_nick_name", pattern="^[a-zA-Z0-9_]*$", max_length=30)
    first_name: str = Field(default="First name", max_length=30, pattern="^[a-zA-Z]*$")
    last_name: str = Field(default="Last name", max_length=50, pattern="^[a-zA-Z]*$")
    email: EmailStr
    hashed_password: str = Field(default="A123B123", pattern="^[a-zA-Z0-9]*$", max_length=9, min_length=8)
    age: int = Field(default=18, gt=17, lt=81, description="Age must be between 18 and 80")
    experience: UserExperience = UserExperience()
    about: str = ""
    head_line: str = Field(default="Last name", max_length=150)

class UserRegestrationModel(BaseModel):
    nick_name: str = Field(default="def_nick_name", pattern="^[a-zA-Z0-9_]*$", max_length=30)
    email: EmailStr = Field(default="def_mail@mail.com")
    hashed_password: str = Field(default="A123B123", pattern="^[a-zA-Z0-9]*$", max_length=9, min_length=8)

class UserLogin(BaseModel):
    user_email: EmailStr = Field(default="def_mail@mail.com")
    hashed_password: str = Field(default="A123B123", pattern="^[a-zA-Z0-9]*$", max_length=9, min_length=8)


#======Return data models==============#
class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class AcceptedUserRegistration(TunedModel):
    nick_name: str = None
    email: str = None

class AcceptedUserDeleted(TunedModel):
    nick_name: str = None
    id:UUID4 = None
    status:str = None

class AcceptedUserGetData(TunedModel):
    id: UUID4 = None
    email: EmailStr = None
    is_active: bool = None
    is_verified: bool = None
    is_superuser: bool = None
    first_name: Union[str | None] = None
    last_name: Union[str | None] = None
    age: int = None
    nick_name: str = None
    position: str = None
    experience: Union[Json | None] = None
    status: str = None
    is_author: bool = None
    about: str = None
    head_line: str = None

class AcceptedUserLogin(TunedModel):
    id: UUID4 = None