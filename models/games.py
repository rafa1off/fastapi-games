from tortoise import models, fields

class Games(models.Model):
    name = fields.CharField(max_length=20)
    genre = fields.CharField(max_length=20)
    platform = fields.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-name']
