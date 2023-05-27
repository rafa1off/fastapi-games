from fastapi import APIRouter, Depends
from middlewares.pagination import pagination
from middlewares.id_validation import id_validation
from models.games import Games, Game
from configs.exceptions import NotFound
from configs.auth import get_current_user

router = APIRouter(
    prefix='/games',
    tags=['games']
)


@router.get('/', response_model=list[Game])
async def games(page_data: dict[str, int] = Depends(pagination)) -> list:
    return await Games.all().limit(page_data['limit']).offset(page_data['skip'])


@router.post('/', status_code=201)
async def add_game(game_data: Game, current_user=Depends(get_current_user)) -> dict:
    try:
        await Games.create(
            name=game_data.name,
            genre=game_data.genre,
            platform=game_data.platform
        )
        return {'message': f'Game {game_data.name} created'}
    except Exception:
        return {'detail': f'Game: {game_data.name} already exists'}


@router.get('/search', response_model=list[Game])
async def search_games(
    page_data: dict[str, int] = Depends(pagination),
    name: str | None = None,
    genre: str | None = None,
    platform: str | None = None
) -> list | None:
    if name:
        return await Games.filter(
            name__icontains=name
        ).limit(page_data['limit']).offset(page_data['skip'])
    elif genre:
        return await Games.filter(
            genre__icontains=genre
        ).limit(page_data['limit']).offset(page_data['skip'])
    elif platform:
        return await Games.filter(
            platform__icontains=platform
        ).limit(page_data['limit']).offset(page_data['skip'])
    else:
        return await Games.all().limit(page_data['limit']).offset(page_data['skip'])


@router.get('/{game_id}', response_model=Game)
async def get_game(game_id: int = Depends(id_validation)) -> Games:
    game = await Games.get_or_none(pk=game_id)
    if game:
        return game
    else:
        raise NotFound(detail='Game not found')


@router.put('/{game_id}')
async def update_game(
    game_data: Game,
    game_id: int = Depends(id_validation),
    current_user=Depends(get_current_user)
) -> dict:
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


@router.delete('/{game_id}')
async def delete_game(
    game_id: int = Depends(id_validation),
    current_user=Depends(get_current_user)
) -> dict:
    game = await Games.get_or_none(pk=game_id)
    if game:
        await game.delete()
        return {'message': f'Game {game.name} removed'}
    else:
        raise NotFound(detail='Game not found')
