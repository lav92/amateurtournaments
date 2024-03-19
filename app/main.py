from fastapi import FastAPI

from app.users.router import router as user_router

app = FastAPI(
    title="Hello World",
)

app.include_router(user_router)


@app.get("/hello")
async def root():
    return "hello"
