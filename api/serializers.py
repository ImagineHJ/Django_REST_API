from rest_framework import serializers
from .models import Profile, Follow, Post, Media, Comment, Like


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' # all fields in the model


class CommentSerializer(serializers.ModelSerializer):
    profile_username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['profile_username', 'text', 'create_date', 'post']

    def get_profile_username(self, obj):
        return obj.profile.user.username


class LikeSerializer(serializers.ModelSerializer):
    profile_username = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['profile_username', 'like_date', 'post']

    def get_profile_username(self, obj):
        return obj.profile.user.username


class PostSerializer(serializers.ModelSerializer):
    # nested Serializer
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    profile_username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'profile_username', 'media_file', 'is_video', 'text', 'create_date', 'comments', 'likes']

    def get_profile_username(self, obj):
        return obj.profile.user.username








