from django_filters.rest_framework import FilterSet, filters
from .models import *


class ContentFilter(FilterSet):
    # video = filters.BooleanFilter(name='is_video')
    following = filters.CharFilter(method='filter_following_contents')

    class Meta:
        model = Content
        fields = ['profile']

    def filter_following_contents(self, queryset, name, value):
        filtered_queryset = queryset.filter(profile__followers__profile=self.request.user)
        return filtered_queryset
