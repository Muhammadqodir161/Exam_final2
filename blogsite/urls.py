
from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts-without-login/', PostViewWithoutLogin.as_view(), name='posts-without-login'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/follow/', FollowToggleView.as_view(), name='follow_toggle'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_update'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),  
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'), 
]
