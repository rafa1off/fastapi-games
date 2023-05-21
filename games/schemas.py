from pydantic import BaseModel

class Game(BaseModel):
    id: int | None = None
    name: str
    genre: str
    platform: str
