from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import os
from dotenv import load_dotenv
load_dotenv()

from routes import index, games

app = FastAPI()

register_tortoise(
    app,
    db_url=os.getenv('POSTGRES_URI'),
    modules={
        'models': ['models.games']
    },
    generate_schemas=True
)

app.include_router(index.router)
app.include_router(games.router)
