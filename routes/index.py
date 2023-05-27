from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def home(nome='Rafael'):
    return {'message': f'Hello {nome}!'}
