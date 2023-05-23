from fastapi import APIRouter, Depends
from middlewares.pagination import pagination
from models.games import Games, Game
from configs.exceptions import BadRequest, NotFound

router = APIRouter(
    prefix='/games',
    tags=['games']
)

@router.get('/', response_model=list[Game])
async def games(page_data: dict[str, int] = Depends(pagination)) -> list:
    return await Games.all().limit(page_data['limit']).offset(page_data['skip'])

@router.post('/', status_code=201)
async def add_game(game_data: Game) -> dict:
    await Games.create(
        name=game_data.name,
        genre=game_data.genre,
        platform=game_data.platform
    )
    return {'message': f'Game {game_data.name} created'}

@router.get('/search', response_model=list[Game])
async def search_games(
    page_data: dict[str, int] = Depends(pagination),
    name: str | None = None,
    genre: str | None = None,
    platform: str | None = None
) -> list:
    if name or genre or platform:
        if name:
            return await Games.filter(name__icontains=name).limit(page_data['limit']).offset(page_data['skip'])
        elif genre:
            return await Games.filter(genre__icontains=genre).limit(page_data['limit']).offset(page_data['skip'])
        else:
            return await Games.filter(platform__icontains=platform).limit(page_data['limit']).offset(page_data['skip'])
    else:
        return await Games.all().limit(page_data['limit']).offset(page_data['skip'])

@router.get('/{game_id}', response_model=Game)
async def get_game(game_id: int) -> Games:
    if game_id >= 1:
        game = await Games.get_or_none(pk=game_id)
        if game:
            return game
        else:
            raise NotFound(detail='Game not found')
    else:
        raise BadRequest(detail='Id must be greater or equal to 1')

@router.put('/{game_id}')
async def update_game(game_id: int, game_data: Game) -> dict:
    if game_id >= 1:
        game = await Games.get_or_none(pk=game_id)
        if game:
            await game.update_from_dict({
                'name': game_data.name,
                'genre': game_data.genre,
                'platform': game_data.platform
            }).save()
            return {'message': f'Game {game.name} updated'}
        else:
            raise NotFound(detail='Game not found')
    else:
        raise BadRequest(detail='Id must be greater or equal to 1')

@router.delete('/{game_id}')
async def delete_game(game_id: int, game_data: Game) -> dict:
    if game_id >= 1:
        game = await Games.get_or_none(pk=game_id)
        if game:
            await game.delete()
            return {'message': f'Game {game_data.name} removed'}
        else:
            raise NotFound(detail='Game not found')
    else:
        raise BadRequest(detail='Id must be greater or equal to 1')
