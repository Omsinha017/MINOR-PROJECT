from django.urls import path
from posts.views import AllPosts, PostDetail, UserPosts, CreatePost, delete_post, post_Comment, LikeView

app_name='posts'

urlpatterns = [
    path("", AllPosts, name="all"),
    path("r/<str:slug>", PostDetail, name="postdetail"),
    path("create", CreatePost, name="create"),
    path("user", UserPosts, name="user"),
    path('delete/<int:id>',delete_post,name='delete'),
    path('postComment',post_Comment, name="postComment"),
    path('like/<int:pk>', LikeView, name='like_post'),

]
