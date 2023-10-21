from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from models.alchemy_models import Seauser
from typing import Union, Tuple


class UserDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def delete(self, user_id:str) -> dict[str:str]:
        action = await self.db_session.execute(update(Seauser)
                                       .where(Seauser.id == user_id)
                                       .values(status = "deleted")
                                       .returning(Seauser.nick_name, Seauser.status, Seauser.id))
        out = {c: v for c, v in zip(action.keys(), action.first())}
        return out

    async def create(self,
                            nick_name: Seauser.nick_name,
                            email: Seauser.email,
                            hashed_password: Seauser.hashed_password) -> dict[str:str]:

        new_user = Seauser(nick_name=nick_name,email=email,
                           hashed_password=hashed_password)

        action = await self.db_session.execute(insert(Seauser).values(nick_name = new_user.nick_name,
                                                                  email = new_user.email,
                                                                  hashed_password = new_user.hashed_password)
                                                            .returning(Seauser.nick_name, Seauser.email))

        out = {c:v for c,v in zip(action.keys(), action.first())}
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

    async def user_change_status(self, user_id:Seauser.id, new_status:Seauser.status) -> Seauser:

        update_status = await self.db_session.execute(update(Seauser)
                                                          .where(Seauser.id == user_id)
                                                          .values(status = new_status)
                                                          .returning(Seauser.status))

        return update_status.scalar()

    async def get_user_data(self, user_id) -> Seauser:
        out = await self.db_session.execute(select(Seauser).where(Seauser.id == user_id))
        print(out.fetchone())
        return out.fetchone()
