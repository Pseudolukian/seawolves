from pydantic import BaseModel, Field, EmailStr, UUID4, Json
from datetime import date
from typing import Union
from datetime import datetime,time
from typing import Optional
from enum import Enum

#================== Input data models =======================#
#============User=============#
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
    nick_name: str = Field(default="def_nick_name", pattern="^[a-zA-Z0-9_]*$", min_length=10, max_length=30)
    first_name: str = Field(default="First name", max_length=30, pattern="^[a-zA-Z]*$")
    last_name: str = Field(default="Last name", max_length=50, pattern="^[a-zA-Z]*$")
    email: EmailStr
    hashed_password: str = Field(default="A123B123", pattern="^[a-zA-Z0-9]*$", min_length=8, max_length=8)
    age: int = Field(default=18, gt=17, lt=81, description="Age must be between 18 and 80")
    experience: UserExperience = UserExperience()
    about: str = ""
    head_line: str = Field(default="Last name", max_length=150)

class UserRegestrationModel(BaseModel):
    nick_name: str = Field(default="def_nick_name", pattern="^[a-zA-Z0-9_]*$", max_length=30)
    email: EmailStr = Field(default="def_mail@mail.com")
    hashed_password: str = Field(default="A123B123", pattern="^[a-zA-Z0-9]*$", min_length=8, max_length=8)

class UserLogin(BaseModel):
    user_email: EmailStr = Field(default="def_mail@mail.com")
    hashed_password: str = Field(default="A123B123", pattern="^[a-zA-Z0-9]*$", min_length=8, max_length=8)
    cookie_name: str = Field(default="SeawolveUserToken")
    cookie_length: int = Field(default=13)

#=============Calendar===================

class CalendarCreate(BaseModel):
    user_id: UUID4 = Field(default=None)
    calendar_name: str = Field(default='My_meets')

class MeetCreate(BaseModel):
    calendar_id: Optional[UUID4] = Field(default=None)
    guest_id: Optional[UUID4] = Field(default=None)
    date_of_meet: date = Field(default_factory=date.today)
    time_of_meet_start: time = Field(default_factory=lambda: time())
    time_of_meet_end: time = Field(default_factory=lambda: time())
    link_to_Google_Meet: Optional[str] = Field(default=None)

    meet_title: str = Field(default='My meet with the best sea mentor in the world')
    meet_agenda: str = Field(default='Become the greatest seawolf.')

#=================== Return data models =======================#
class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class AcceptedUserRegistration(TunedModel):
    nick_name: str = None
    email: str = None
    id: UUID4 = None

class AcceptedUserDeleted(TunedModel):
    nick_name: str = None
    id:UUID4 = None
    status:str = None

class AcceptedUserUpdateStatusModel(TunedModel):
    status: str = None

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

class AcceptedUserLogout(TunedModel):
    message: str = "You are logout."

#=======Calendar=========

class AcceptedCalendarCreate(TunedModel):
    message: str = 'Calendar created.'