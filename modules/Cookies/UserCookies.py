from fastapi import Request, Response
from models.pydantic_models import UserLogin
from pydantic import UUID4


class UserCookies:
    def __init__(self):
        pass

    async def check_cookie_login(self, request: Request, cookie_options: UserLogin) -> bool:
        check_cookie = request.cookies.get(str(cookie_options.cookie_name))
        return bool(check_cookie)

    async def set_cookie_login(self, response: Response, request: Request, cookie_options: UserLogin, user_id: UUID4):
        cookie_check = await self.check_cookie_login(request=request, cookie_options=cookie_options)
        if cookie_check:
            pass
        else:
            return response.set_cookie(key=cookie_options.cookie_name, value=str(user_id["id"]).replace('-', ''))

    async def del_cookie_login(self, response: Response, cookie_options: UserLogin):
        return response.delete_cookie(key=cookie_options.cookie_name)