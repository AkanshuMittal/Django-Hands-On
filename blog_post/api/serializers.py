from rest_framework import serializers
from django.contrib.auth.models import User
from posts.models import Post, Category


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    author_name   = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model  = Post
        fields = [
            'id', 'title', 'content',
            'author', 'author_name',
            'category', 'category_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']