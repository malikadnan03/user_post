from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from .models import Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, post_id):
        post = self.get_object(post_id)
        self.check_object_permissions(request, post)

        serializer = PostSerializer(post, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, post_id):
        post = self.get_object(post_id)
        self.check_object_permissions(request, post)

        post.delete()
        return Response({"detail": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def get_object(self, post_id):
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found")

    def check_object_permissions(self, request, post):
        if post.user != request.user:
            raise PermissionDenied(detail="You don't have permission to perform this action.")

class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = self.get_post(post_id)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, post_id, comment_id):
        post = self.get_post(post_id)
        comment = self.get_comment(comment_id)

        # Check if the request user is the author of the comment or the post
        if request.user != comment.user and request.user != post.user:
            raise PermissionDenied(detail="You don't have permission to edit this comment.")

        serializer = CommentSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, post_id, comment_id):
        post = self.get_post(post_id)
        comment = self.get_comment(comment_id)

        # Check if the request user is the author of the comment or the post
        if request.user != comment.user and request.user != post.user:
            raise PermissionDenied(detail="You don't have permission to delete this comment.")

        comment.delete()
        return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def get_post(self, post_id):
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise NotFound(detail="Post not found")

    def get_comment(self, comment_id):
        try:
            return Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found")
