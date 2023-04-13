from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'followers', 'followings']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_at']

class OnlyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment', ]


class PostSerializer(serializers.ModelSerializer):
    comments = OnlyCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'comments']
