from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

#=======Input data models===========#
class UserExperience(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    position: str = ""
    responsibilities: str = ""

class UserBaseInputModel(BaseModel):
    email: EmailStr
    hashed_password: str = "12345678"
    first_name: str = Field(default="First name", max_length=30, pattern="^[a-zA-Z]*$")
    last_name: str = Field(default="Last name", max_length=50, pattern="^[a-zA-Z]*$")
    age: int = Field(default=18, gt=17, lt=81, description="Age must be between 18 and 80")
    nick_name: str = Field(default="def_nick_name", pattern="^[a-zA-Z0-9_]*$", max_length=30)
    experience: UserExperience = UserExperience()
    about: str = ""
    head_line: str = Field(default="Last name", max_length=150)

class UserRegestrationModel(BaseModel):
    nick_name: str = Field(default="def_nick_name", pattern="^[a-zA-Z0-9_]*$", max_length=30)
    email: EmailStr
    hashed_password: str = "12345678"


#======Return data models==============#
class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class AcceptedUserRegistration(TunedModel):
    nick_name: str = None
    email: str = None

