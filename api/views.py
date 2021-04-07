# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from .models import Post
from .serializers import PostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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


class PostList(APIView):

    def get(self, request, format=None):
        post = Post.objects.all()  # get queryset of the Post
        serializer = PostSerializer(post, many=True)  # Serialize it to python native data type
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
