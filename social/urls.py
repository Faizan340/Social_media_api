from django.urls import path, include
from .views import UserProfileView, FollowView, UnfollowView, CreatePostView, DeletePostView, CommentPostView, AllPostsView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'social'

urlpatterns = [
    path('api/authenticate/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/authenticate/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', UserProfileView.as_view(), name='get-user'),
    path('api/follow/<int:id>/', FollowView.as_view(), name='follow-user'),
    path('api/unfollow/<int:id>/', UnfollowView.as_view(), name='unfollow-user'),
    path('api/posts/', CreatePostView.as_view(), name='create_post_api'),
    path('api/posts/<int:id>/', DeletePostView.as_view(), name='delete_post_api'),
    path('api/comment/<int:id>/', CommentPostView.as_view(), name='create_comment_api'),
    path('api/all_posts/', AllPostsView.as_view(), name='all-posts'),
]
