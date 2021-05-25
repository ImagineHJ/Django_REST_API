from rest_framework import serializers
from .models import Profile, Follow, Content, Media, Comment, Like


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # fields = '__all__' # all fields in the model

        fields = ['username', 'password', 'first_name', 'last_name', 'bio', 'website', 'profile_img', 'private']


class FollowSerializer(serializers.ModelSerializer):
    profile_username = serializers.SerializerMethodField()
    followed_username = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['profile', 'profile_username', 'followed', 'followed_username']

    def get_profile_username(self, obj):
        return obj.profile.username

    def get_followed_username(self, obj):
        return obj.followed.username

    def validate(self, data):
        if data['profile'] == data['followed']:
            raise serializers.ValidationError("Can't follow myself")
        return data


class CommentSerializer(serializers.ModelSerializer):
    profile_username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['content', 'profile', 'profile_username', 'text', 'created_at']

    def get_profile_username(self, obj):
        return obj.profile.username


class LikeSerializer(serializers.ModelSerializer):
    profile_username = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['content', 'profile', 'profile_username', 'created_at', ]

    def get_profile_username(self, obj):
        return obj.profile.username


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['content', 'media_idx', 'media_file', 'is_video']


class ContentSerializer(serializers.ModelSerializer):
    # nested Serializer
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    medias = MediaSerializer(many=True, read_only=True)
    profile_username = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['profile', 'profile_username', 'media_file',
                  'is_video', 'text', 'created_at', 'comments', 'likes', 'medias']

    def get_profile_username(self, obj):
        return obj.profile.username









