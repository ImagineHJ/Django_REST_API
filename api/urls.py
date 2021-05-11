from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework import routers
from .views import PostViewSet

'''
urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>', views.PostDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
'''

router = routers.DefaultRouter()
router.register(r'Post', PostViewSet)   # register()함으로써 두 개의 url 생성

urlpatterns = router.urls
