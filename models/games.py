from tortoise import models, fields
from pydantic import BaseModel


class Games(models.Model):
    name = fields.CharField(max_length=20, unique=True)
    genre = fields.CharField(max_length=20)
    platform = fields.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']


class Game(BaseModel):
    id: int | None = None
    name: str
    genre: str
    platform: str

    class Config:
        orm_mode = True
