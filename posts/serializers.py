from . models import Post
from rest_framework import serializers
from categories.models import Category


class PostSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'body',
            'owner',
            'categories'
        )