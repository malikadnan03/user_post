# account/urls.py
from django.urls import path
from .views import RegisterView, PostView, CommentView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name="sign_up"),
    path('api/posts/', PostView.as_view(), name="post-list"),
    path('api/posts/<int:post_id>/', PostView.as_view(), name="post-detail"),
    path('api/posts/<int:post_id>/comments/', CommentView.as_view(), name="post-comments"),
    path('api/posts/<int:post_id>/comments/<int:comment_id>/', CommentView.as_view(), name="comment-detail"),
]
