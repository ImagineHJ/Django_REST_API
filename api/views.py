from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Post
from .serializers import PostSerializer

# Create your views here.

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
