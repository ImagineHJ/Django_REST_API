# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from .models import Post
from .serializers import PostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
'''
# Use CVB instead of FCV

@csrf_exempt
def post_list(request):
    """
    List all code posts, or create a new post.
    """
    # view data
    if request.method == 'GET':
        post = Post.objects.all()  # get queryset of the Post
        serializer = PostSerializer(post, many=True)  # Serialize it to python native data type
        return JsonResponse(serializer.data, safe=False)  # response with JSON

    # add data
    elif request.method == 'POST':
        data = JSONParser().parse(request)  # parse the JSON data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # save to DB
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
'''

'''
# Use viewsets instead of APIview

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Renders to content type as requested by the client

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
'''


class PostFilter(FilterSet):
    video = filters.BooleanFilter(name='is_video')
    following = filters.CharFilter(method='filter_following_posts')

    class Meta:
        model = Post
        fields = ['profile']

    def filter_following_posts(self, queryset, name, value):
        filtered_queryset = queryset.filter(profile__following__followers=self.request.user)
        return filtered_queryset


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend]



