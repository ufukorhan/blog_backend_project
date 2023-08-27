from . models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'body',
            'owner',
            'comments',
            'categories',
            'created_at',
            'updated_at'
        ]


