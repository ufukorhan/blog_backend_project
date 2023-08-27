from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    CASCADE
)
from utils.models import BaseModel


class Post(BaseModel):
    title = CharField(max_length=100, null=False, blank=False)
    body = TextField(null=False, blank=False)
    owner = ForeignKey('auth.User', related_name='posts', on_delete=CASCADE)

    class Meta:
        ordering = ['-created_at']
