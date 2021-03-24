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

공식문서 참조 :https://docs.djangoproject.com/ko/3.0/ref/models/fields

1. User
```class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.TextField(max_length=10)
    bio = models.TextField()
    profile_img = models.ImageField(blank=True)
    post_num = models.IntegerField()
    follower_num = models.IntegerField()
    following_num = models.IntegerField()
```

2.
```
class Follow(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    follower_user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    followed_date = models.DateTimeField(auto_now_add=True)
```

3.
```
class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    like_num = models.IntegerField()
    comment_num = models.IntegerField()
    media_num = models.IntegerField()
```

```
class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    media_file = models.FileField()
    is_video = models.BooleanField()

```

```
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    text = models.TextField()
```

```
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
```


### ORM 적용해보기
shell에서 작성한 코드와 그 결과를 보여주세요!

### 간단한 회고
과제 시 어려웠던 점이나 느낀 점, 좋았던 점 등을 간단히 적어주세요!
