# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(AbstractUser, Base):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)  # OneToOne Link with User Model
    website = models.TextField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_img = models.ImageField( upload_to="profile_img")  # save to media/profile_img
    private = models.BooleanField(default=False)

    # post_num = models.IntegerField(default=0)
    # follower_num = models.IntegerField(default=0)
    # following_num = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Follow(Base):  # profile follows followed_user_id
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="following")
    followed_user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="followers")
    # followed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} followed {}'.format(self.profile.username, self.followed_user_id.username)


class Content(Base):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    # create_date = models.DateTimeField(auto_now_add=True)
    # update_date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=500, blank=True)
    # like_num = models.IntegerField(default=0)
    # comment_num = models.IntegerField(default=0)
    # media_num = models.IntegerField(default=1)  # at least one media


    # Add (a post requires at least one media)
    media_file = models.FileField(upload_to="post_media")  # first/thumbnail media, save to media/post_media
    is_video = models.BooleanField()  # file can be either img or vid

    def __str__(self):
        return 'post{}, {} by {}'.format(self.id, self.text, self.profile.username)


class Media(Base):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="media")
    media_idx = models.IntegerField()  # idx of media in the post 2~10
    media_file = models.FileField(upload_to="post_media")  # save to media/post_media
    is_video = models.BooleanField()  # file can be either img or vid

    def __str__(self):
        return '{}th media of post: {}'.format(self.media_num, self.post.text)


class Comment(Base):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="comments")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    # create_date = models.DateTimeField(auto_now_add=True)
    # update_date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'comment: {} on post{} by {}'.format(self.text, self.content.id, self.profile.username)


class Like(Base):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="likes")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    # like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'like on post: {} by {}'.format(self.content.id, self.profile.username)