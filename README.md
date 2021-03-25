# CEOS 13기 백엔드 스터디
## REST API 서버 개발
### 인스타그램 클론

## 유의사항
* 본 레포지토리는 백엔드 스터디 2-3주차의 과제를 위한 레포입니다.
* 따라서 해당 레포를 fork 및 clone 후 local에서 본인의 깃헙 ID 브랜치로 작업한 후 커밋/푸시하고, PR 보낼 때도 `본인의 브랜치-> 본인의 브랜치`로 해야 합니다.

## 2주차 과제 (기한: 3/25 목요일까지)
### 모델 설명
인스타그램에 대해 본인이 작성한 모델들에 대한 설명과 모델 간의 관계 등을 적어주세요!

< 모델 빌딩>


* 인스타그램을 사용자 및 게시 기준으로 분석 
  
    **사용자** : 이름, 아이디, 웹사이트, 소개, 프로필 사진, 게시물, 팔로워, 팔로잉 -> 여러개의 팔로잉, 및 게시글

    **게시물** : 사진 및 영상, 설명글, 작성자, 좋아요, 댓글 -> 여러개의 좋아요 및 댓글 


<img width="400" alt="inst_model_1" src="https://user-images.githubusercontent.com/57395765/112103234-ce066380-8bec-11eb-8c66-3bce6d7c905b.png">
<img width="390" alt="inst_model_2" src="https://user-images.githubusercontent.com/57395765/112103255-d52d7180-8bec-11eb-9fd3-b6435505c96a.png">




* 데이터 모델 다이어그램

<img width="700" src="https://user-images.githubusercontent.com/57395765/112107489-55a2a100-8bf2-11eb-9204-0b2724f8af82.png">


<모델 구현>

Field 관련 공식문서 참조 : https://docs.djangoproject.com/ko/3.0/ref/models/fields

#### 1. User
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # OneToOne Link with User Model
    website = models.TextField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_img = models.ImageField(blank=True)
    post_num = models.IntegerField()
    follower_num = models.IntegerField()
    following_num = models.IntegerField()

    def __str__(self):
        return self.user.username
```
* User Model 관련 공식 문서 참조 : https://docs.djangoproject.com/en/3.1/ref/contrib/auth/
* Django의 User Model에는 username, first_name, last_name, email, password, groups, last_login, date_joined ...등 필드 지원  
* User에서 제공하는 필드 이외에 필요한 필드 작성

#### 2. Follow
```python
class Follow(models.Model):  # profile follows followed_user_id
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="following")
    followed_user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="followers")
    followed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} followed {}'.format(self.profile.user.username, self.followed_user_id.user.username)
```
* 한 유저가 다른 유저를 팔로우하는 것을 모델화, FK 사용 
* related_name : profile에서 쉽게 역참조 가능
* __str__(): 문자열 포맷팅 사용으로 누가 누구를 팔로우 하는지 표현 
* 다른 방법 : ManyToMany Relation으로 User에 follower, following field 추가



#### 3. Post
```python
class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=500, blank=True)
    like_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    media_num = models.IntegerField(default=1)  # at least one media
    
    # Add (a post requires at least one media)
    media_file = models.FileField()  # first media
    is_video = models.BooleanField()  # file can be either img or vid

    def __str__(self):
        return 'post: {} by {}'.format(self.text, self.profile.user.username)
```
* 최소 하나의 사진/영상이 있어야 하기 때문에 대표 미디어 파일 포함 
* str(): 포스팅 텍스트와 사용자를 표현

#### 4. Media
```python
class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
    media_num = models.IntegerField()  # num of media in the post 2~10
    media_file = models.FileField()
    is_video = models.BooleanField()  # file can be either img or vid

    def __str__(self):
        return '{}th media of post: {}'.format(self.media_num, self.post.text)
```
* 한 포스팅에는 최대 10개의 사진/영상이 업로드, FK사용 -> 개수 제한을 어떻게 할
* 기본 미디어 이외에 추가적인 미디어를 업로드할 때 사용 

#### 5. Comment
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'comment: {} on post: {} by {}'.format(self.text, self.post.text, self.profile.user.username)
```
* 한 포스팅에 여러개의 댓글 존재, FK 사용
* 한 유저가 여러개의 댓글 게시 가능, FK 사용 
* str(): 누가 어느 포스팅에 어느 댓글을 남겼는지 표현 

#### 6. Like
```python
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'like on post: {} by {}'.format(self.post.text, self.profile.user.username)
```
* 한 포스팅에 여러개의 좋아요 존재, FK 사용
* 한 유저가 여러개의 좋아요 가능, FK 사용

#### Migration
* ImageField를 지원하기 위해서 Pillow 설치:
```python -m pip install Pillow```
  

* ```python manage.py makemigrations api```
  
* ```python manage.py migrate```

### ORM 적용해보기
shell에서 작성한 코드와 그 결과를 보여주세요!

### 간단한 회고
과제 시 어려웠던 점이나 느낀 점, 좋았던 점 등을 간단히 적어주세요!
