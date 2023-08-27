from django.db import models
from utils.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=100, blank=False, default='')
    owner = models.ForeignKey('auth.User', related_name='categories', on_delete=models.CASCADE)
    posts = models.ManyToManyField('posts.Post', related_name='categories', blank=True)

    class Meta:
        verbose_name_plural = 'categories'
