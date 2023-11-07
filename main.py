from fastapi import FastAPI, APIRouter
import uvicorn
from routers.user_router import user_router
from fastapi.responses import PlainTextResponse
from pydantic import ValidationError

main_api_router = APIRouter()
app = FastAPI()

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)




if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8003, reload=True)

