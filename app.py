from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def home(nome='Rafael'):
    return {'message': f'Hello {nome}!'}
