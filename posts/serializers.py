from . models import Post
from rest_framework import serializers
from categories.models import Category
from comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'body',
            'owner',
            'categories',
            'comments'
        )
        read_only_fields = [
            'id',
            'comments',
            'owner',
            'created_at',
            'updated_at'
        ]
        