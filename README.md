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
    profile_img = models.ImageField(blank=True, upload_to="profile_img")  # save to media/profile_img
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
Q: 두 방법의 차이점과, 장단점, 어느 방법이 많이 쓰이는지 궁금합니다.



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
    media_file = models.FileField(upload_to="post_media")  # first/thumbnail media, save to media/post_media
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
    media_file = models.FileField(upload_to="post_media")  # save to media/post_media
    is_video = models.BooleanField()  # file can be either img or vid

    def __str__(self):
        return '{}th media of post: {}'.format(self.media_num, self.post.text)
```
* 한 포스팅에는 최대 10개의 사진/영상이 업로드, FK사용 
* 기본 미디어 이외에 추가적인 미디어를 업로드할 때 사용 
* Q: 한 포스팅에는 최소 1개 최대 10개의 사진/영상이 존재할 수 있다. 
  최소조건을 구현하기 위해 Post 모델에 미디어 파일을 추가했는데,
  이 방법이 최선의 방법인지, 다른 방법이 있을까..?
  또한 최대 9개의 미디어만이 한 포스팅에 존재할 수 있는데, FK의 개수를 제한할 수 있는 방법은 무엇일까,,,
* Q: 미디어 파일이 사진인지 영상인지를 구분하기 위해 boolean 필드를 사용했는데, 필요한 작업인지..?
   (필요할 거 같아서 추가한거긴 하지만 확실하지 않아서,,) 그냥 FileField만 있으면 충분한지...

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
<img width="800" alt="migration" src="https://user-images.githubusercontent.com/57395765/112435881-aa782000-8d88-11eb-9a0c-a38659467cf8.png">

### ORM 적용해보기
shell에서 작성한 코드와 그 결과를 보여주세요!
* user 생성 및 profile 생성 : username이 'user1'이고 이름이 'John Kim'인 사용자 생성 <br></br>
<img width="645" alt="create user" src="https://user-images.githubusercontent.com/57395765/112436066-e7441700-8d88-11eb-81f3-0eedfe6c57fa.png">


* user1의 게시물 3개 생성<br><br>
  * "This is the picture of me with my pet dog" (사진)<br></br>
  * "An old family picture of my childhood" (영상) <br></br>
  * "I went to DisneyLand! Miss those times...:(" (사진)<br></br>
<img width="904" alt="create posts" src="https://user-images.githubusercontent.com/57395765/112436074-e8754400-8d88-11eb-8443-3ad86ae82ec0.png">


* filter를 사용해 게시물 조회 <br></br>
  * 사진만 올라간 게시물 : ```Post.objects.filter(is_video=False)```<br></br>
  * user1이 작성한 게시물 : ```Post.objects.filter(profile__user__username="user1")```<br></br>
  * 설명이 "This is"로 시작하는 게시물 : ```Post.objects.filter(text__startswith='This is')```<br></br>
<img width="896" alt="filter1" src="https://user-images.githubusercontent.com/57395765/112436076-e90dda80-8d88-11eb-97b3-54afce98d50e.png">
<img width="898" alt="filter2" src="https://user-images.githubusercontent.com/57395765/112436077-e90dda80-8d88-11eb-973a-1ba5ad12ea6e.png">

### 간단한 회고
첫 주차 보다 Django가 어떤 시스템으로 돌아가는지 알 수 있었고, 
특히 데이터 모델링 관련한 경험을 할 수 있어서 좋았다. 단순히 필요한 데이터를 저장하는게 아니라, 
이를 효율적으로 구성하고 관리할 수 있도록 모델링하는 과정이 흥미로우면서 어려웠다. 아직 다양한 Django 코드를
볼 기회가 많지 않아서, 모델링하면서도 나의 모델링 방식이 효율적인건지 더 좋은 대안이 있는지 궁금했다.
모델링 전 다이어그램을 작성한 것은 데이터를 구성하는데 정말 도움이 됐고, 코드를 작성할 때도 편했다. 
직접 SQL를 사용하지 않고 모델링 및 마이그레이션을 통해 데이터 베이스 테이블을 생성하고 Django ORM으로 데이터를 생성할 수 있어서 편했다. 

추가로 공부할 것

* 좋은 프로그래머들이 작성한 다양한 데이터 모델링 코드를 본다.
* 헷갈리는 Relation 개념에 대해 추가 공부를 한다.


## 3주차 과제 (기한: 4/1 목요일까지)
### 모델 선택 및 데이터 삽입
선택한 모델의 구조와 데이터 삽입 후의 결과화면을 보여주세요!

```python
class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=500, blank=True)

    # Add (a post requires at least one media)
    media_file = models.FileField(upload_to="post_media")  # first/thumbnail media, save to media/post_media
    is_video = models.BooleanField()  # file can be either img or vid

    def __str__(self):
        return 'post{}, {} by {}'.format(self.id, self.text, self.profile.user.username)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'comment: {} on post{} by {}'.format(self.text, self.post.id, self.profile.user.username)
```


```python
>>> Post.objects.all()
<QuerySet 
[<Post: post1, This is the picture of me with my pet dog by user1>, 
<Post: post2, An old family video of my childhood! by user1>, 
<Post: post3, I went to DisneyLand! Miss those times...:( by user1>]>

>>> Comment.objects.all()
<QuerySet 
[<Comment: comment: Looking good! on post1 by user2>, 
<Comment: comment: Your dog is so cute >_< on post1 by user2>]>

```
* 3개의 post, post1에 달린 2개의 comment

```python
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
```

* nested serializer로 post의 comments, likes까지 serialize
* 알아보기 쉽도록, serializer method field로 post 작성자의 username 가져옴
* fields에 '\_\_all\_\_'을 작성했다가, 인스타그램을 참고해서 노출되는 필드만을 설정

### 모든 list를 가져오는 API
```python
# api/views.py

@csrf_exempt
def post_list(request):
    # view data
    if request.method == 'GET':
        post = Post.objects.all()  # get queryset of the Post
        serializer = PostSerializer(post, many=True)  # Serialize it to python native data type
        return JsonResponse(serializer.data, safe=False)  # response with JSON

```
  
* **JsonResponse**: dictionary, list 등 python data type을 JSON 형식으로 변환
  변환할 데이터가 dictionary가 아닌 경우 ```safe=False``` 설정 
* **CSRF(Cross Site Request Forgery)**: 사용자의 의지와 무관하게 request에 요청을 보내도록 하는 해킹 수법, Django에서는 CSRF방어를 내장기능으로 지원하고 있음
* `````@csrf_exempt````` : 개발 시 불편함을 해결하기 위해 함수 상단에 작성해, CSRF 방어 해제 



```python
# api/urls.py

urlpatterns = [
    path('posts/', views.post_list)
]
```
```python
# config/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```
* **include()**: 일치하는 문자열 자르고, 뒤 문자열은 api의 url conf로 전달
* ```/api/posts/```가 되면 views.py의 post_list() 호출 

<API 요청 결과>
* URL: ```api/posts/```
* Method: ```GET```

```json
[
    {
        "id": 1,
        "profile_username": "user1",
        "media_file": null,
        "is_video": false,
        "text": "This is the picture of me with my pet dog",
        "create_date": "2021-03-25T16:28:53.833162+09:00",
        "comments": [
            {
                "profile_username": "user2",
                "text": "Looking good!",
                "create_date": "2021-03-31T18:42:36.646261+09:00",
                "post": 1
            },
            {
                "profile_username": "user2",
                "text": "Your dog is so cute >_<",
                "create_date": "2021-03-31T18:43:28.014466+09:00",
                "post": 1
            }
        ],
        "likes": []
    },
    {
        "id": 2,
        "profile_username": "user1",
        "media_file": null,
        "is_video": true,
        "text": "An old family video of my childhood!",
        "create_date": "2021-03-25T16:30:49.907742+09:00",
        "comments": [],
        "likes": []
    },
    {
        "id": 3,
        "profile_username": "user1",
        "media_file": null,
        "is_video": false,
        "text": "I went to DisneyLand! Miss those times...:(",
        "create_date": "2021-03-25T16:31:42.307405+09:00",
        "comments": [],
        "likes": []
    }
]
```
* 모든 post의 list를 가져오는 API 요청 


### 새로운 데이터를 create하도록 요청하는 API


```python
# api/views.py

def post_list(request):
  ...
    # add data
    elif request.method == 'POST':
        data = JSONParser().parse(request)  # parse the JSON data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # save to DB
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
```

* 파싱한 JSON data를 받아서 deserialize한 후 valid data 체킹 
* 잘 설계된 REST API는 URI만 잘 설계된 것이 아닌 그 리소스에 대한 응답을 잘 내어주는 것도 포함 
* **201 상태 코드**: 클라이언트가 어떠한 리소스 생성을 요청, 해당 리소스가 성공적으로 생성됨(POST를 통한 리소스 생성 작업 시)
* **400 상태 코드**: 클라이언트의 요청이 부적절 할 경우 사용하는 응답 코드


<API 요청 결과>
* URL: ```api/posts/```
* Method: ```POST```
* Body:```
   {
        "profile_username": "user1",
        "text": "I am studying at a cafe, right now",
        "is_video": false,
        "media_file" : null,
        "profile" : 1
    }```



```json
{
      "id": 4,
      "profile_username": "user1",
      "media_file": null,
      "is_video": false,
      "text": "I am studying at a cafe, right now",
      "create_date": "2021-04-01T17:42:45.143591+09:00",
      "comments": [],
      "likes": []
}
```



### 공부한 내용 정리


#### [GET]
* GET은 서버로부터 정보를 조회하기 위해 설계된 메소드
* GET은 요청을 전송할 때 필요한 데이터를 Body에 담지 않고, 쿼리스트링(URL의 끝에 ?와 함께 이름과 값으로 쌍을 이루는 요청 파라미터)
)을 통해 전송
  
* 데이터 이동이 없을 때, DB에 영향을 주지 않을 때 주로 사용, 따로 설정하지 않으면 항상 GET 요청 사용 
* **Idempotent** : GET은 설계원칙에 따라 서버의 데이터나 상태를 변경시키지 않아야하기 때문에 주로 조회를 할 때에 사용






#### [POST]
* POST는 리소스를 생성/변경하기 위해 설계되어 전송해야될 데이터를 HTTP 메세지의 Body에 담아서 전송
* Body는 길이의 제한이 없어 POST 요청은 대용량 데이터를 전송하는데 적합
* DB에 영향을 줄 때나, URL에 노출이 되면 안전하지 못한 데이터를 전송할 때 사용
* 따로 POST 방식으로 설정해야 사용할 수 있음
* **Non-idempotent** : 서버에게 동일한 요청을 여러 번 전송해도 응답은 항상 다를 수 있어서 서버의 상태나 데이터를 변경시킬 때 사용



[**[출처]**](https://blog.naver.com/astro0/222293557953)

### 간단한 회고

실습 자체는 예시 코드를 참고할 수 있어서 어렵지 않았지만 Serialize, REST 라는 개념이 확 와닿지 않았다. 
이해도를 높일 수 있는 좋은 블로그 글을 찾았고, 전반적으로 웹 서비스가 어떻게 돌아가는지 이해할 수 있었다.

[**[참고한 블로그]**](https://post.naver.com/viewer/postView.nhn?volumeNo=30717005&memberNo=6457418&vType=VERTICAL)

* 서버와 클라이언트가 소통할 때는 API를 사용하고, API의 파일 형식은 JSON, 개발자들 사이에서 규격화된 API의 형식이 REST(GET, POST)이다. 
* python 기반인 django 서버에서는 클라이언트한테 보내는 데이터를 python data type으로 Serialize(변환?)하고, Serialize된 데이터를 JSON으로 렌더링해서 클라이언트에게 보내준다. 
* 반대로 클라이언트에게서 데이터를 받는 경우에는 JSON을 파싱한 후, Deserialize해서 DB에 이를 저장한다.



## 4주차 과제 (기한: 4/8 목요일까지)

### CVB
이전 코드 DRF에서 제공하는 CVB로 수정
```python
# api/views.py

# def post_list(request):
class PostList(APIView):
    # if request.method == 'GET':
    def get(self, request, format=None):
        post = Post.objects.all()  # get queryset of the Post
        serializer = PostSerializer(post, many=True)  # Serialize it to python native data type
        # return JsonResponse(serializer.data, safe=False)  # response with JSON
        return Response(serializer.data) # Renders to content type as requested by the client

    # elif request.method == 'POST':
    def post(self, request, format=None):
        # data = JSONParser().parse(request)  # parse the JSON data
        # serializer = PostSerializer(data=data)
        serializer = PostSerializer(data=request.data)  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods
        if serializer.is_valid():
            serializer.save()  # save to DB
            # return JsonResponse(serializer.data, status=201)
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
* request.data : JSON 이외의 형식을 가진 파일도 처리 
* Response() : 요청한 데이터 타입으로 렌더링 (JSON 형식에 한정되지 않음)
* request, response에서 JSON으로 한정된 파일 형식 -> 해결 



특정 Post에 관한 요청을 처리하는 클래스 추가 
```python
class PostDetail(APIView):

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)  # pass the instance we want to update and new data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

* url에서 pk를 파라미터로 전달받음
* 모든 메소드에서 custom 함수 get_object를 호출해 전달받은 pk값을 가진 객체를 받는다 / 없는 경우 에러 처리 -> CBV의 재사용성
* PUT : Serializer를 호출할 때 update하고자 하는 객체와 새로운 데이터를 인자로 전달
* DELETE : ORM delete()를 이용해서 DB에서 삭제 

```python
# urls.py

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>', views.PostDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

* \<int:pk\> : URL의 정수 값을 pk라는 이름으로 받아서 view로 전
* as_view() : dispatch() 호출 -> request에 따라 get(), post() 등 호출
* 파일 확장자를 URL 뒤에 붙여, 파일 형식을 명시하는 경우가 많다. (예. 'http://example.com/api/users.json') 하지만 일일히 이를 URLconf에 패턴으로 등록하기 어려움 <br>
-> **format_suffix_patterns** : 파일 확장명이 뒤에 붙은 URL을 등록 및 처리할 수 있도록 함 (해당 view 함수에 format argument 지정해야 함 )

### 모든 list를 가져오는 API
* URL: ```api/posts/```
* Method: ```GET```
```json
[
    {
        "id": 1,
        "profile_username": "user1",
        "media_file": null,
        "is_video": false,
        "text": "This is the picture of me with my pet dog",
        "create_date": "2021-03-25T07:28:53.833162",
        "comments": [
            {
                "profile_username": "user2",
                "text": "Looking good!",
                "create_date": "2021-03-31T09:42:36.646261",
                "post": 1
            },
            {
                "profile_username": "user2",
                "text": "Your dog is so cute >_<",
                "create_date": "2021-03-31T09:43:28.014466",
                "post": 1
            }
        ],
        "likes": []
    },
    {
        "id": 2,
        "profile_username": "user1",
        "media_file": null,
        "is_video": true,
        "text": "An old family video of my childhood!",
        "create_date": "2021-03-25T07:30:49.907742",
        "comments": [],
        "likes": []
    },
    {
        "id": 3,
        "profile_username": "user1",
        "media_file": null,
        "is_video": false,
        "text": "I went to DisneyLand! Miss those times...:(",
        "create_date": "2021-03-25T07:31:42.307405",
        "comments": [],
        "likes": []
    },
    {
        "id": 4,
        "profile_username": "user1",
        "media_file": null,
        "is_video": false,
        "text": "I am studying at a cafe, right now",
        "create_date": "2021-04-01T08:42:45.143591",
        "comments": [],
        "likes": []
    }
]
```

### 특정 데이터를 가져오는 API
* URL: ```api/posts/1```
* Method: ```GET```
```json
{
    "id": 1,
    "profile_username": "user1",
    "media_file": null,
    "is_video": false,
    "text": "This is the picture of me with my pet dog",
    "create_date": "2021-03-25T07:28:53.833162",
    "comments": [
        {
            "profile_username": "user2",
            "text": "Looking good!",
            "create_date": "2021-03-31T09:42:36.646261",
            "post": 1
        },
        {
            "profile_username": "user2",
            "text": "Your dog is so cute >_<",
            "create_date": "2021-03-31T09:43:28.014466",
            "post": 1
        }
    ],
    "likes": []
}
```

### 새로운 데이터를 생성하는 API
* URL: ```api/posts/```
* Method: ```POST```
* Body
<img width="1234" alt="스크린샷 2021-04-07 오후 6 44 34" src="https://user-images.githubusercontent.com/57395765/113848920-ee7d1300-97d3-11eb-9f24-dd5240d588b3.png">
```json
{
    "id": 5,
    "profile_username": "user2",
    "profile": 2,
    "media_file": "/media/post_media/IMG_5527_4FTlMUl.JPG",
    "is_video": false,
    "text": "\"I went to London last year\"",
    "create_date": "2021-04-07T18:49:07.433259",
    "comments": [],
    "likes": []
}
```

### 특정 데이터를 업데이트하는 API

* URL: ```api/posts/```
* Method: ```PUT```
* Body
<img width="1195" alt="스크린샷 2021-04-07 오후 7 00 48" src="https://user-images.githubusercontent.com/57395765/113848935-f2a93080-97d3-11eb-85d8-5987a2a93a70.png">
```json
{
    "id": 4,
    "profile_username": "user1",
    "profile": 1,
    "media_file": null,
    "is_video": false,
    "text": "I am relaxing at a cafe near my home",
    "create_date": "2021-04-01T08:42:45.143591",
    "comments": [],
    "likes": []
}
```
* profile 필드에 값을 필수로 넣어주어야 한다 (FK로 연결된 필드여서 그런 것 같다...)

### 특정 데이터를 삭제하는 API
요청 URL 및 delete된 결과를 보여주세요!
* URL: ```api/posts/2```
* Method: ```DELETE```
```json
[
    {
        "id": 1,
        "profile_username": "user1",
        "profile": 1,
        "media_file": null,
        "is_video": false,
        "text": "This is the picture of me with my pet dog",
        "create_date": "2021-03-25T07:28:53.833162",
        "comments": [
            {
                "profile_username": "user2",
                "text": "Looking good!",
                "create_date": "2021-03-31T09:42:36.646261",
                "post": 1
            },
            {
                "profile_username": "user2",
                "text": "Your dog is so cute >_<",
                "create_date": "2021-03-31T09:43:28.014466",
                "post": 1
            }
        ],
        "likes": []
    },
    {
        "id": 3,
        "profile_username": "user1",
        "profile": 1,
        "media_file": null,
        "is_video": false,
        "text": "I went to DisneyLand! Miss those times...:(",
        "create_date": "2021-03-25T07:31:42.307405",
        "comments": [],
        "likes": []
    },
    {
        "id": 4,
        "profile_username": "user1",
        "profile": 1,
        "media_file": null,
        "is_video": false,
        "text": "I am relaxing at a cafe near my home",
        "create_date": "2021-04-01T08:42:45.143591",
        "comments": [],
        "likes": []
    },
    {
        "id": 5,
        "profile_username": "user2",
        "profile": 2,
        "media_file": "/media/post_media/IMG_5527_4FTlMUl.JPG",
        "is_video": false,
        "text": "\"I went to London last year\"",
        "create_date": "2021-04-07T18:49:07.433259",
        "comments": [],
        "likes": []
    }
]
```

### 공부한 내용 정리
새로 알게된 점, 정리 하고 싶은 개념, 궁금한점 등을 정리해 주세요

### 간단한 회고
Django 개발 중 view 파트가 가장 핵심적이면서도 어려운 것 같다. 지금까지 개발한 API 서버의 동작 과정을 정리해보았다. 

1. 클라이언트가 URL에 접속 
2. 서버에 request가 옴
3. URLconf가 문자열 비교를 통해 해당 URL에 지정된 view를 호출 (이때 인자 값을 넘겨줄 수 있음)
4. view에서는 데이터 처리 등 다양한 작업이 이루지고 -> 이후 클라이언트에게 다시 response 보냄
5. 프론트엔드에서 이를 적절히 처리해서 사용자에게 보여줌 

view에서도 확실히 클래스 기반 뷰가 효율적일 것 같다. 클래스에서 함수나 변수를 정의해 이를 여러 메소드에서 사용할 수 있을 것 같다. 뷰를 더 효율적으로 작성할 수 있도록 많은 연습과 공부가 필요할 것 같다.



