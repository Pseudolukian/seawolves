from sqlalchemy import select, update, insert, Result
from sqlalchemy.ext.asyncio import AsyncSession
from models.alchemy_models import Seauser
from pydantic import UUID4, BaseModel
from typing import Type
from models.pydantic_models import AcceptedUserDeleted, AcceptedUserRegistration, UserRegestrationModel, UserDeleteModel




class UserDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def _sql_return_parser(self, sql_return: Result, output_model: Type[BaseModel]) -> Type[BaseModel]:
        row = sql_return.fetchone()
        result_out = {}

        if row:
            mid_res = row[0].__dict__.copy()
            mid_res.pop('_sa_instance_state', None)

            for field_name in output_model.model_fields.keys():
                if field_name in mid_res:
                    result_out[field_name] = mid_res[field_name]

            return result_out
        else:
            return None

    async def delete(self, user_id:UUID4) -> AcceptedUserDeleted:
        request = update(Seauser).where(Seauser.id == user_id).values(status="deleted").returning(Seauser)
        action = await self.db_session.execute(request)
        out = await self._sql_return_parser(sql_return=action, output_model=AcceptedUserDeleted)
        return out

    async def create(self, nick_name: str, email: str, password: str) -> AcceptedUserRegistration:
        new_user = UserRegestrationModel(nick_name=nick_name, emai=email, hashed_password=password)
        request = insert(Seauser).values(nick_name=new_user.nick_name, email=new_user.email, hashed_password=new_user.hashed_password).returning(Seauser)
        action = await self.db_session.execute(request)
        out = await self._sql_return_parser(sql_return=action, output_model=AcceptedUserRegistration)
        return out



    async def update(self, user_id_to_update: Seauser.id = None,
                     nick_name_to_update: Seauser.nick_name = None,
                     first_name_to_update: Seauser.first_name = None,
                     last_name_to_update: Seauser.last_name = None,
                     email_to_update: Seauser.email = None,
                     hashed_pass_to_update: Seauser.hashed_password = None,
                     age_to_update: Seauser.age = None,
                     exp_to_update: Seauser.experience = None,
                     about_to_update: Seauser.about = None,
                     head_line_to_update: Seauser.head_line = None) -> Seauser:

        values_to_update = {
            "nick_name": nick_name_to_update,
            "first_name": first_name_to_update,
            "last_name": last_name_to_update,
            "email": email_to_update,
            "hashed_password": hashed_pass_to_update,
            "age": age_to_update,
            "experience": exp_to_update,
            "about": about_to_update,
            "head_line": head_line_to_update
        }

        actual_updates = {key: value for key, value in values_to_update.items() if value is not None}

        if not actual_updates:
            raise ValueError("No values provided for update.")

        action = await self.db_session.execute(
            update(Seauser)
            .where(Seauser.id == user_id_to_update)
            .values(**actual_updates)
            .returning(*[getattr(Seauser, k) for k in actual_updates.keys()])
        )

        return action.scalar()

    async def user_change_status(self, user_id: Seauser.id, new_status: Seauser.status) -> Seauser:

        update_status = await self.db_session.execute(update(Seauser)
                                                          .where(Seauser.id == user_id)
                                                          .values(status = new_status)
                                                          .returning(Seauser.status))

        return update_status.scalar()

    async def get_user_data(self, user_id: Seauser.id) -> Seauser:
        request = select(Seauser).where(Seauser.id == user_id)
        out = await self.db_session.execute(request)
        out = out.first()[0].__dict__.copy()
        out.pop('_sa_instance_state', None)
        return out

    async def user_log_in(self, user_email: Seauser.email, hashed_password: Seauser.hashed_password) -> Seauser:
        request = select(Seauser.id).where(Seauser.email == user_email, Seauser.hashed_password == hashed_password)
        out = await self.db_session.execute(request)




