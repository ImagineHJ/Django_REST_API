from rest_framework import serializers
from .models import Profile, Follow, Post, Media, Comment, Like


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # nested Serializer
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    profile_username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'  # all fields in the model

    def get_profile_username(self, obj):
        return obj.profile.user.username








