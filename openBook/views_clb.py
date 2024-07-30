from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.views import LogoutView
from django.views.generic import DeleteView

from users.models import Post, CustomUser, Follow, Topic, Share, Like, Comment
from .forms import SignUpForm, PasswordRecovery, CustomUserForm, CustomProfileForm
from .utils import activate_email

class CustomHomeView(LoginRequiredMixin, View):
    def get(self, request):
        search_query = request.GET.get('q', '')
        posts = Post.objects.filter(Q(text__icontains=search_query) | Q(topic__name__icontains=search_query))
        topics = Topic.objects.all()
        users_to_follow = CustomUser.objects.exclude(id=request.user.id)
        followed_users_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
        users_to_follow_result = users_to_follow.exclude(id__in=followed_users_ids)

        context = {
            'posts': posts,
            'topics': topics,
            'users_to_follow_result': users_to_follow_result,
        }

        return render(request, 'home.html', context)
    
    def post(self, request):
        user = request.user
        content = request.POST.get('content')
        topic = request.POST.get('topic')
        image = request.FILES.get('add_photo')

        if not content:
            messages.info(request, 'The content field is required')
            return redirect('home')
        
        if not Topic.objects.filter(name=topic).exists():
            new_topic = Topic.objects.create(name=topic)
        else:
            new_topic = Topic.objects.get(name=topic)

        new_post = Post.objects.create(
            user=user,
            text=content,
            topic=new_topic,
            image=image,
        )

        if new_post is not None:
            new_post.save()

            return redirect('home')

class CustomLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, 'Your already logged in, Logout first to sign in class')
            return redirect('home')
        
        return render(request, 'login.html')
        
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = authenticate(request, email=email, password=password)
        except:
            user = None

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

class CustomLogoutView(LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)

class CustomRegisterView(View):
    def get(self, request):
        form = SignUpForm()
        if request.user.is_authenticated:
            messages.warning(request, 'Your already logged in, Logout first to sign up')
            return redirect('home')
        
        context = {
            'form': form,
        }
        return render(request, 'register.html', context)
        
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('complete_profile')
        else:
            messages.error(request, 'Invalid')
            return redirect('register')

class PasswordRecoveryEmailView(View):
    def get(self, request):
        form = PasswordRecovery()
        context = {
            'form': form,
        }

        return render(request, 'password_recovery_email.html', context)
    
    def post(self, request):
        if request.method == 'POST':
            form = PasswordRecovery(request.POST)
            if form.is_valid():
                user_email = form.cleaned_data.get('email')
                associated_user = get_user_model().objects.filter(Q(email=user_email)).first()

                if associated_user:
                    activate_email(request=request, user=associated_user, receiver=user_email)
                    return redirect('password_recovery_email')

            else:
                return redirect('password_recovery_email')

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        target_post = self.get_object()
        if request.user.id != target_post.user.id:
            messages.warning(request, "You don't have the permission to perform this action")
            return redirect('home')
        
        messages.success(request, "The post has ben deleted")
        return redirect('home')
        
    def get(self, request):
        pass

class EditPostView(LoginRequiredMixin, View):
    model = Post
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        image = request.FILES.get('add_photo')
        text = request.POST.get('content')
        topic = request.POST.get('topic')
        clear_image = request.POST.get('clearImage')

        pk = self.kwargs.get('pk')

        post = get_object_or_404(Post, pk=pk)

        if request.user != post.user:
            messages.warning(request, "You don't have the permission to perform this action")
            return redirect('home')
        
        if clear_image == 'on':
            post.image = None
        else:
            if image:
                post.image = image
            else:
                post.image = None

        post.text = text
        if Topic.objects.filter(name=topic).exists():
            topic_obj = get_object_or_404(Topic, name=topic)
        else:
            topic_obj = Topic.objects.create(name=topic)

        post.topic = topic_obj

        messages.success(request, 'Post has been successfully updated')
        post.save()

        return redirect('home')

class SettingsView(LoginRequiredMixin, View):
    template_name = 'settings.html'

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user_form = CustomUserForm(instance=user)
        profile_form = CustomProfileForm(instance=user.profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }

        return render(request, self.template_name, context)

class UpdateProfileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(CustomUser, pk=pk)
        avatar = request.FILES.get('avatar')
        name = request.POST.get('name')
        bio = request.POST.get('bio')

        if avatar:
            user.profile.avatar = avatar


        user.profile.name = name
        user.profile.bio = bio
        user.save()

        messages.success(request, 'You has been successfully Updated You Profile credentials')

        return redirect('settings', user.id)

class CompleteProfileView(LoginRequiredMixin, View):
    def post(self, request):
        user = get_object_or_404(CustomUser, pk=request.user.pk)
        
        avatar = request.FILES.get('avatar')
        name = request.POST.get('name')
        bio = request.POST.get('bio')

        if avatar:
            user.profile.avatar = avatar

        if not name:
            messages.warning(request, 'Full name is required')
            return redirect('complete_profile')


        user.profile.name = name
        user.profile.bio = bio
        user.save()
        messages.success(request, 'You has been successfully Completed You Profile credentials')
        return redirect('home')
    
    def get(self, request):
        form = CustomProfileForm(instance=request.user.profile)
        context = {
            'form': form,
        }

        return render(request, 'complete_profile.html', context)

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(CustomUser, id=request.user.pk)
        posts = Post.objects.filter(user=user)
        shared_posts = Share.objects.filter(user=user)
        followers = user.followers.all()
        following = user.following.all()

        context = {
            'posts': posts,
            'shared_posts': shared_posts,
            'followers': followers,
            'following': following,
        }

        return render(request, 'profile.html', context)

class UserView(LoginRequiredMixin, View):
    def get(self, request):
        users = CustomUser.objects.all().exclude(id=request.user.id)
        followed_users_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)


        return render(request, 'users_view.html', {'users': users, "followed_users_ids": followed_users_ids})

class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        chosen_user = CustomUser.objects.get(id=pk)
        following = Follow.objects.create(
            follower=request.user,
            following=chosen_user
        )
        following.save()
        messages.success(request, f'You has been successfully followed {chosen_user.username}')

        return redirect('home')

class UnFollowUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        chosen_user = CustomUser.objects.get(id=pk)
        following = Follow.objects.get(follower=request.user, following=chosen_user)
        following.delete()

        messages.success(request, f'You has been successfully UNfollowed {chosen_user.username}')
        return redirect('home')
    
class LikingPostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = request.user
        post = get_object_or_404(Post, id=pk)
        like_action = Like.objects.create(
            user=user,
            post=post,
        )
        like_action.save()
        messages.success(request, 'You has been successfully liked this post')
        return redirect('home')

class UnLikingPostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, id=pk)
        like_action = Like.objects.get(post=post, user=request.user)
        like_action.delete()

        messages.success(request, 'You has been successfully Unlike this post')
        return redirect('home')

class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = request.user
        target_post = Post.objects.get(id=pk)
        new_comment_text = request.POST.get('create_comment')
        new_comment = Comment.objects.create(
            user=user,
            post=target_post,
            text=new_comment_text,
        )

        new_comment.save()
        messages.success(request, 'You has been successfully created a comment on this post')

        return redirect('home')

class SharePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = request.user
        target_post = Post.objects.get(id=pk)

        new_share = Share.objects.create(
            user=user,
            post=target_post,
        )

        new_share.save()

        messages.success(request, 'You has been successfully Shared this post')

        return redirect('home')