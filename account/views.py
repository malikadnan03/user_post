from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import PermissionDenied, NotFound
from .models import Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)  
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@permission_classes([IsAuthenticated])
@api_view(['PUT', 'DELETE'])
def post_detail(request, post_id):
    post = get_post(post_id)
    check_object_permissions(request, post)

    if request.method == 'PUT':
        return update_post(request, post)
    elif request.method == 'DELETE':
        return delete_post(request, post)    

def update_post(request, post):
    serializer = PostSerializer(post, data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

def delete_post(request, post):
    post.delete()
    return Response({"detail": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

def get_post(post_id):
    try:
        return Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise NotFound(detail="Post not found")

def check_object_permissions(request, post):
    if post.user != request.user:
        raise PermissionDenied(detail="You don't have permission to perform this action.")

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_comment(request, post_id):
    post = get_post(post_id)

    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user, post=post)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@permission_classes([IsAuthenticated])
@api_view(['PUT', 'DELETE'])
def comment_detail(request, post_id, comment_id):
    post = get_post(post_id)
    comment = get_comment(comment_id)

    check_comment_permissions(request, comment, post)

    if request.method == 'PUT':
        return update_comment(request, comment)
    elif request.method == 'DELETE':
        return delete_comment(request, comment)

def update_comment(request, comment):
    serializer = CommentSerializer(comment, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

def delete_comment(request, comment):
    comment.delete()
    return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

def get_comment(comment_id):
    try:
        return Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        raise NotFound(detail="Comment not found")

def check_comment_permissions(request, comment, post):
    if request.user != comment.user and request.user != post.user:
        raise PermissionDenied(detail="You don't have permission to perform this action.")
