from fastapi import FastAPI, APIRouter
import uvicorn
from routers.user_router import user_router

main_api_router = APIRouter()
app = FastAPI()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)

