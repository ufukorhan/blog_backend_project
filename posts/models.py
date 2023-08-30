from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    ManyToManyField,
    CASCADE
)
from utils.models import BaseModel
from categories.models import Category


class Post(BaseModel):
    title = CharField(max_length=100, null=False, blank=False)
    body = TextField(null=False, blank=False)
    owner = ForeignKey('auth.User', related_name='posts', on_delete=CASCADE)
    categories = ManyToManyField(Category)

    class Meta:
        ordering = ['-created_at']
