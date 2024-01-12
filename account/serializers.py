# serializers.py
from rest_framework import serializers
from .models import UserData, Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]
        extra_kwargs = {'password': {'write_only': True}}  # To ensure password is write-only

    def create(self, validated_data):
        user = UserData.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class CommentSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(source='content')  # Rename 'content' to 'comment'

    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'created_at']
        read_only_fields = ['created_at', 'user']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'user', 'comments']
        read_only_fields = ['created_at', 'user', 'comments']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance 
