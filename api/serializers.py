from rest_framework import serializers
from .models import Profile, Follow, Content, Media, Comment, Like


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' # all fields in the model


class CommentSerializer(serializers.ModelSerializer):
    profile_username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['profile_username', 'text', 'created_at', 'content']

    def get_profile_username(self, obj):
        return obj.profile.username



class LikeSerializer(serializers.ModelSerializer):
    profile_username = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['profile_username', 'created_at', 'content']

    def get_profile_username(self, obj):
        return obj.profile.username


class ContentSerializer(serializers.ModelSerializer):
    # nested Serializer
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    profile_username = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'profile_username', 'profile', 'media_file', 'is_video', 'text', 'created_at', 'comments', 'likes']

    def get_profile_username(self, obj):
        return obj.profile.username









