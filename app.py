from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import os
from dotenv import load_dotenv
load_dotenv()

from routes import games

app = FastAPI()

register_tortoise(
    app,
    db_url=os.getenv('POSTGRES_URI'),
    modules={
        'models': ['games.models']
    },
    generate_schemas=True
)

@app.get('/')
async def home(nome='Rafael'):
    return {'message': f'Hello {nome}!'}

app.include_router(games.router)
