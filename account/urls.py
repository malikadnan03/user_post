# account/urls.py
from django.urls import path
from .views import register_user, post_list, post_detail, create_comment, comment_detail
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', register_user, name="sign_up"),
    path('api/posts/', post_list, name="post-list"),
    path('api/posts/<int:post_id>/', post_detail, name="post-detail"),
    path('api/posts/<int:post_id>/comments/', create_comment, name="post-comments"),
    path('api/posts/<int:post_id>/comments/<int:comment_id>/', comment_detail, name="comment-detail"),
]
