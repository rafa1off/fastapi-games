from fastapi import APIRouter, Depends
from models.users import UserIn, Users, User
from configs.exceptions import Forbidden
from fastapi.security import OAuth2PasswordRequestForm
from configs.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    hash_password,
    Token
)

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.get('/', response_model=User)
async def get_user(current_user: User = Depends(get_current_user)):
    return await Users.get(pk=current_user.username)


@router.post('/')
async def create_user(user_data: UserIn):
    hashed_pwd = hash_password(user_data.password)
    await Users.create(
        username=user_data.username,
        name=user_data.name,
        hashed_password=hashed_pwd
    )
    return {'message': f'User {user_data.name} created'}


@router.post('/login', response_model=Token)
async def login(user_data: OAuth2PasswordRequestForm = Depends()):
    user = await Users.get_or_none(pk=user_data.username)
    if user:
        authenticated: bool = authenticate_user(user_data.password, user.hashed_password)
        if not authenticated:
            raise Forbidden(detail='Invalid password')
        else:
            access_token = create_access_token(
                data={'sub': user.username}
            )
            return {'access_token': access_token, 'token_type': 'bearer'}
    else:
        raise Forbidden(detail='Invalid username')
