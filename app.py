from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from configs.tortoise import TORTOISE_ORM
from routes import index, games, users

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
)

app.include_router(index.router)
app.include_router(games.router)
app.include_router(users.router)
