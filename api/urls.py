from django.urls import path
import views

urlpatterns = [
    path('posts/', views.post_list)
]