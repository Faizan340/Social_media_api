from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile, Post, Comment
from .serializers import UserProfileSerializer, PostSerializer, CommentSerializer


class FollowView(APIView):
    """
    API view to follow a user.
    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        """
        Handle POST requests to follow a user.
        :param request: HTTP request object
        :param id: ID of the user to follow
        """
        user_to_follow = User.objects.get(id=id)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.followings.add(user_to_follow)
        user_to_follow_profile = UserProfile.objects.get(user=user_to_follow)
        user_to_follow_profile.followers.add(request.user)
        return Response(status=200)


class UnfollowView(APIView):
    """
    API view to unfollow a user.
    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        """
        Handle POST requests to unfollow a user.
        :param request: HTTP request object
        :param id: ID of the user to unfollow
        """
        user_to_unfollow = User.objects.get(id=id)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.followings.remove(user_to_unfollow)
        user_to_unfollow_profile = UserProfile.objects.get(user=user_to_unfollow)
        user_to_unfollow_profile.followers.remove(request.user)
        return Response(status=200)


class UserProfileView(APIView):
    """
    API view to retrieve a user's profile.
    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests to retrieve a user's profile.

        :param request: HTTP request object
        """
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        print(user_profile)
        return Response(serializer.data)
    

class CreatePostView(generics.CreateAPIView):
    """
    API view to create a new post.

    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new post.

        :param request: HTTP request object
        :param args: additional arguments
        :param kwargs: additional keyword arguments
        """
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeletePostView(generics.DestroyAPIView):
    """
    API view to delete a post.

    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve a post.

        :param request: HTTP request object
        :param args: additional arguments
        :param kwargs: additional keyword arguments
        """
        post = get_object_or_404(Post, id=kwargs['id'], author=request.user)
        serializer = PostSerializer(post)
        return Response(
            {
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests to retrieve a post.

        :param request: HTTP request object
        :param args: additional arguments
        :param kwargs: additional keyword arguments
        """
        post = get_object_or_404(Post, id=kwargs['id'], author=request.user)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentPostView(generics.CreateAPIView):
    """
    API view to post a comment.

    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to post a new comment.

        :param request: HTTP request object
        :param args: additional arguments
        :param kwargs: additional keyword arguments
        """
        post = get_object_or_404(Post, id=kwargs['id'])
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AllPostsView(generics.ListAPIView):
    """
    API view to retrieve all the posts.

    Requires authentication.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset of all the posts.
        """
        user = self.request.user
        posts = Post.objects.all().order_by('-created_at')
        return posts

    def list(self, request, *args, **kwargs):
        """
        Returns a serialized list of posts with their comments.

        :param request: HTTP request object.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.

        :return: Serialized list of posts with their comments.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = []
        for post_data in serializer.data:
            post_id = post_data['id']
            comments = Comment.objects.filter(post_id=post_id).values_list('comment', flat=True)
            post_data['comments'] = list(comments)
            data.append(post_data)
        return Response({'data': data})
