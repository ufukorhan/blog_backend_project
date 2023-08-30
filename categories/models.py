from django.db import models
from utils.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=100, blank=False, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
