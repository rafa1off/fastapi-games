from fastapi import APIRouter, HTTPException
from models.games import Games, Game

router = APIRouter(
    prefix='/games',
    tags=['games']
)

@router.get('/', response_model=list[Game])
async def games(limit: int = 5, page: int = 1) -> list:
    if limit >= 0 and page >= 1:
        skip = limit * (page - 1)
        return await Games.all().limit(limit).offset(skip)
    else:
        raise HTTPException(status_code=400,
                            detail='Limit must be greater or equal to 0'
                            ' and page greater or equal to 1')

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
    limit: int = 5,
    page: int = 1,
    name: str | None = None,
    genre: str | None = None,
    platform: str | None = None
) -> list:
    if limit >= 0 and page >= 1:
        skip = limit * (page - 1)
        if name or genre or platform:
            if name:
                return await Games.filter(name__icontains=name).limit(limit).offset(skip)
            elif genre:
                return await Games.filter(genre__icontains=genre).limit(limit).offset(skip)
            else:
                return await Games.filter(platform__icontains=platform).limit(limit).offset(skip)
        else:
            return await Games.all().limit(limit).offset(skip)
    else:
        raise HTTPException(status_code=400,
                            detail='Limit must be greater or equal to 0'
                            ' and page greater or equal to 1')

@router.get('/{game_id}', response_model=Game)
async def get_game(game_id: int) -> Games:
    if game_id >= 1:
        game = await Games.get_or_none(pk=game_id)
        if game:
            return game
        else:
            raise HTTPException(status_code=404, detail='Game not found')
    else:
        raise HTTPException(status_code=400,
                            detail='Id must be greater or equal to 1')

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
            raise HTTPException(status_code=404, detail='Game not found')
    else:
        raise HTTPException(status_code=400,
                            detail='Id must be greater or equal to 1')

@router.delete('/{game_id}')
async def delete_game(game_id: int, game_data: Game) -> dict:
    if game_id >= 1:
        game = await Games.get_or_none(pk=game_id)
        if game:
            await game.delete()
            return {'message': f'Game {game_data.name} removed'}
        else:
            raise HTTPException(status_code=404, detail='Game not found')
    else:
        raise HTTPException(status_code=400,
                            detail='Id must be greater or equal to 1')
