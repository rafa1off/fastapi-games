from fastapi import APIRouter
from games.schemas import Game
from games.models import Games

router = APIRouter(
    prefix='/games',
    tags=['games']
)

@router.get('/', response_model=None)
async def games(limit=5, page=1) -> list[Games]:
    skip = limit * (page - 1)
    list_games = await Games.all().limit(limit).offset(skip)
    return list_games

@router.post('/')
async def add_game(game: Game) -> dict:
    await Games.create(
        name=game.name,
        genre=game.genre,
        platform=game.platform
    )
    return {'message': f'Game {game.name} created'}

@router.get('/{game_id}', response_model=None)
async def get_game(game_id: int) -> Games | dict:
    game = await Games.get_or_none(pk=game_id)
    if game:
        return game
    else:
        return {'message': 'Game not found'}

@router.put('/{game_id}')
async def update_game(game_id: int, game_data: Game) -> dict:
    game = await Games.get_or_none(pk=game_id)
    if game:
        await game.update_from_dict({
            'name': game_data.name,
            'genre': game_data.genre,
            'platform': game_data.platform
        }).save()
        return {'message': f'Game {game.name} updated'}
    else:
        return {'message': 'Game not found'}

@router.delete('/{game_id}')
async def delete_game(game_id: int, game_data: Game) -> dict:
    game = await Games.get_or_none(pk=game_id)
    if game:
        await game.delete()
        return {'message': f'Game {game_data.name} removed'}
    else:
        return {'message': 'Game not found'}
