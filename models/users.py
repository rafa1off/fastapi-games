from tortoise import models, fields
from pydantic import BaseModel


class Users(models.Model):
    username = fields.CharField(max_length=20, pk=True, unique=True)
    name = fields.CharField(max_length=20)
    hashed_password = fields.CharField(max_length=100)

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ["username"]


class User(BaseModel):
    username: str
    name: str | None = None

    class Config:
        orm_mode = True


class UserIn(User):
    password: str

    class Config:
        orm_mode = True
