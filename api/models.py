# Create your models here.

# models.py

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.TextField()
    bio = models.TextField()
    profile_img = models.ImageField(blank=True)
    post_num = models.IntegerField()
    follower_num = models.IntegerField()
    following_num = models.IntegerField()

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    follower_user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    followed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} followed {}'.format(self.follower_user_id.user.username, self.profile.user.username)


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    like_num = models.IntegerField()
    comment_num = models.IntegerField()
    media_num = models.IntegerField()

    def __str__(self):
        return 'post: {} by {}'.format(self.text, self.profile.user.username)


class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    media_num = models.IntegerField()  # num of media in the post 1~10
    media_file = models.FileField()
    is_video = models.BooleanField()

    def __str__(self):
        return '{}th media of post: {}'.format(self.media_num, self.post.text)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        return 'comment: {} on post: {} by {}'.format(self.text, self.post.text, self.profile.user.username)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'like on post: {} by {}'.format(self.post.text, self.profile.user.username)