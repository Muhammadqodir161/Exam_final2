from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Subscription, Notification
from .forms import PostForm, CommentForm, ProfileForm


class HomePageView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author__profile__followers=self.request.user.profile).order_by('-created_at')

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class ProfileView(DetailView):
    model = Profile
    template_name = 'profile.html'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(Profile, user__username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.get_object().user)
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_form.html'

    def get_object(self):
        return self.request.user.profile
    
class FollowToggleView(LoginRequiredMixin, DetailView):
    model = Profile

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user__username=kwargs['username'])
        if profile.user != request.user:
            if request.user in profile.followers.all():
                profile.followers.remove(request.user)
            else:
                profile.followers.add(request.user)
                Notification.objects.create(user=profile.user, notif_type='follow', from_user=request.user)
        return redirect('profile', username=profile.user.username)