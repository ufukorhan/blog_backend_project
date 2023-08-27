from django.db import models
from utils.models import BaseModel


class Comment(BaseModel):
    body = models.TextField(blank=False)
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']