from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'owner',
            'posts',
            'created_at'
        ]
        
