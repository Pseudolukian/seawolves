# Концепции работы backend SeaWolves

Элементы backend SeaWolves:
* FastAPI – backend framework.
* SQLAlchemy – ORM система.
* PostgreSQL – СУБД.
* boto3 – AWS S3 SDK.
* unicorn – async WYSGIN server.

## Как работает движок SeaWolves {# fast-api-structure}

Движок SeaWolves выполнен на FastAPI (Starlet + Pydantic), а бизнеслогика его работы разделена по слоям:
* [Route](#route--route) – самый верхний слой. В нём реализована логика работы с HTTP-запросами. Route-слой состоит 
  из набора ендпоинтов и правил роутинга.  
* [Control](#control--control) – средний слой. В нём реализована основная логика работы движка: работа с условиями, исключениями, вызов 
  сторонних функций. 
* DAL – самый низкий слой. В нём реализована работа с базой данных – ООП ORM SQL-запросы к СУБД.

### Route {# route}

Ендпоинты (URL) разделены по группам через создание разных инстансов класса `APIRouter()`. Например роутинг 
ендпоинтов по работе с пользователями выглядит так:
```python
from fastapi import APIRouter, Depends
from models.pydantic_models import AcceptedUserRegistration, UserRegestrationModel

from controls.user.User_controls import UserControl
from controls.calendar.Calendar_controls import CalendarControl
from db.session import get_db
from db.user.User_DAL import UserDAL
from db.calendar.Calendar_DAL import Calendar_DAL
from modules.S3.s3 import S3, s3_session

s3_con = s3_session
s3_work = S3(session=s3_con, s3_conf_path='./modules/S3/S3_structure.cfg')
user_router = APIRouter()
user_dal = UserDAL(db_session=get_db)
calendar_dal = Calendar_DAL(db_session=get_db)
user = UserControl(db_connection=get_db, user_dal=user_dal)
calendar = CalendarControl(db_connection=get_db, calendar_dal=calendar_dal)

@user_router.post("/sign-up", response_model=AcceptedUserRegistration)
async def create_user(user_reg_data: UserRegestrationModel = Depends(UserRegestrationModel)) -> AcceptedUserRegistration:
    new_user = await user.create_user(nick_name=user_reg_data.nick_name, email=user_reg_data.email, password=user_reg_data.hashed_password)
    await calendar.calendar_create(user_id=new_user['id'], calendar_name=user_reg_data.nick_name + '\'s calendar' )
    await s3_work.create_structure(bucket_name='seausers', structure_name='sea_user', id=new_user['id'])
    return new_user
...
```

Rout-функции определяют:
* поля форм ендпоинтов (`user_reg_data: UserRegestrationModel = Depends(UserRegestrationModel)`).
* структуру ответа `response_model=AcceptedUserRegistration`.
* вызываемые внутри них control- и module-функции.

В rout-функции  

Далее инстанс `user_router` подключается к root-роутеру в main-файле проекта FastAPI:
```python
from fastapi import FastAPI, APIRouter
import uvicorn
from routers.user_router import user_router

main_api_router = APIRouter()
app = FastAPI()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8003, reload=True)
```

### Control {# control}

