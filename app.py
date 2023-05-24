from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from configs.tortoise import TORTOISE_ORM
from routes import index, games

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True
)

app.include_router(index.router)
app.include_router(games.router)
