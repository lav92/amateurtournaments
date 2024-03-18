from fastapi import FastAPI


app = FastAPI(
    title="Hello World",
)


@app.get("/hello")
async def root():
    return "hello"
