from controls.user.User_controls import UserControl
from db.user.User_DAL import UserDAL
from db.session import get_db
from models.pydantic_models import UserRegestrationModel,AcceptedUserRegistration
from models.alchemy_models import Seauser
import asyncio

db_connection = get_db()
user_dal_instence = UserDAL(db_session=db_connection)
user_control_instence = UserControl(db_connection=db_connection, user_dal=user_dal_instence)

async def pseudo_router_create_user(nick_name:Seauser.nick_name,
                                  email: Seauser.email, hashed_password: Seauser.hashed_password):
    user = await user_control_instence.create_user(nick_name=nick_name, email=email, hashed_password=hashed_password, input_model=UserRegestrationModel)


    print(user)




if __name__ == "__main__":
    asyncio.run(pseudo_router_create_user(nick_name="test_nick_name_23", email="test_mail_23@mail.com", hashed_password="3432424232"))
    #asyncio.run(test_update_user_data(user_id_to_update="51ce233e-3e40-42c7-91da-284ce45003d2", age=20, nick_nam="Pseudo"))
    #asyncio.run(test_create_user(nick_name="some_nick5", email="some@mail5.com", hashed_password="324324234"))
    #asyncio.run(test_delete_user(user_id_to_delete="5dc6279f-1f27-4d95-b502-124b0c55b70c"))