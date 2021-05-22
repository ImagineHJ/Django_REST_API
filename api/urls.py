from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework import routers
from .views import ProfileViewSet, FollowViewSet, ContentViewSet, MediaViewSet, CommentViewSet, LikeViewSet

'''
urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>', views.PostDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
'''

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewSet)   # register()함으로써 두 개의 url 생성
router.register(r'follow', FollowViewSet)
router.register(r'content', ContentViewSet)
router.register(r'media', MediaViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'like', LikeViewSet)



urlpatterns = router.urls
