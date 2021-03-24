# Create your models here.

# models.py

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # OneToOne Link with User Model
    website = models.TextField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_img = models.ImageField(blank=True)
    post_num = models.IntegerField(default=0)
    follower_num = models.IntegerField(default=0)
    following_num = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Follow(models.Model):  # profile follows followed_user_id
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="following")
    followed_user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="followers")
    followed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} followed {}'.format(self.profile.user.username, self.follower_user_id.user.username)


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=500, blank=True)
    like_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    media_num = models.IntegerField()  # at least one media

    def __str__(self):
        return 'post: {} by {}'.format(self.text, self.profile.user.username)


class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
    media_num = models.IntegerField()  # num of media in the post 1~10
    media_file = models.FileField()
    is_video = models.BooleanField()  # file can be either img or vid

    def __str__(self):
        return '{}th media of post: {}'.format(self.media_num, self.post.text)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'comment: {} on post: {} by {}'.format(self.text, self.post.text, self.profile.user.username)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'like on post: {} by {}'.format(self.post.text, self.profile.user.username)