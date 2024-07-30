from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import SignUpForm, PasswordRecovery, SetPasswordForm, TinymceForm, CustomUserForm, CustomProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode

from .tokens import account_activation_token
from .utils import activate_email
from users.models import Post, Topic, CustomUser, Follow, Like, Comment, Share, Message

from django.http import JsonResponse

import json

User = get_user_model()

@login_required(login_url='login')
def home_view(request):
    search_query = request.GET.get('q', '')
    posts = Post.objects.filter(Q(text__icontains=search_query) | Q(topic__name__icontains=search_query))
    topics = Topic.objects.all()
    users_to_follow = CustomUser.objects.exclude(id=request.user.id)
    followed_users_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    users_to_follow_result = users_to_follow.exclude(id__in=followed_users_ids)


    if request.method == 'POST':
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

    context = {
        'posts': posts,
        'topics': topics,
        'users_to_follow_result': users_to_follow_result,
    }

    return render(request, 'home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Your already logged in, Logout first to sign in')
        return redirect('home')
    
    if request.method == 'POST':
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

    return render(request, 'login.html')

@login_required(login_url='login')
def logout_view(request):
    messages.success(request, 'Your successfully logged out')
    logout(request)

    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Your already logged in, Logout first to sign up')
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('complete_profile')
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }

    return render(request, 'register.html', context)

def password_recovery_email_view(request):
    if request.method == 'POST':
        form = PasswordRecovery(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()

            if associated_user:
                activate_email(request=request, user=associated_user, receiver=user_email)

        else:
            messages.error(request, "this email does not exists")

    else:
        form = PasswordRecovery()
    
    context = {
        'form': form,
    }
    
    return render(request, 'password_recovery_email.html', context)

# Not done
def password_recovery_view(request, uuidb64, token):
    try:
        uid = urlsafe_base64_decode(uuidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been set. You can now log in.')
                return redirect('login')
        else:
            form = SetPasswordForm(user)

        return render(request, 'password_recovery.html', {'form': form})
    else:
        messages.error(request, 'The password reset link was invalid.')
        return redirect('password_reset')

@login_required(login_url='login')
def delete_post_view(request, pk):
    if request.method == 'POST':
        target_post = get_object_or_404(Post, pk=pk)
        if request.user != target_post.user:
            messages.warning(request, "You don't have the permission to perform this action")
            return redirect('home')

        target_post.delete()
        messages.success(request, 'The post has been successfully deleted')

    return redirect('home')

@login_required(login_url='login')
def edit_post_view(request, pk):
    if request.method == 'POST':
        image = request.FILES.get('add_photo')
        text = request.POST.get('content')
        topic = request.POST.get('topic')
        clear_image = request.POST.get('clearImage')

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

# here
@login_required(login_url='login')
def settings_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user_form = CustomUserForm(instance=user)
    profile_form = CustomProfileForm(instance=user.profile)


    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'settings.html', context)

# Not Done
@login_required(login_url='login')
def update_user_view(request, pk):
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    old_email = user.email
    old_username = user.username
    
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.warning(request, 'Password do not match')
            return redirect('settings', user.username)
        
        if username != old_username:
            if CustomUser.objects.filter(username=username).exists():
                messages.warning(request, 'This username is already taken.')
                return redirect('settings', user.username)
        if email != old_email:
            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request, 'This email is already taken.')
                return redirect('settings', user.username)
            
        user.email = email
        user.username = username
        user.set_password(password1)

        user.save()
        messages.success(request, 'You has been successfully Updated You User credentials')
    
    return redirect('settings', user.id)

@login_required(login_url='login')
def update_profile_view(request, pk):
    user = get_object_or_404(CustomUser, pk=request.user.pk)

    if request.method == 'POST':
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

@login_required(login_url='login')
def complete_profile_view(request):
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    form = CustomProfileForm(instance=user.profile)

    if request.method == 'POST':
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

    context = {
        'form': form,
    }

    return render(request, 'complete_profile.html', context)

@login_required(login_url='login')
def profile_view(request):
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

@login_required(login_url='login')
def users_view(request):
    users = CustomUser.objects.all().exclude(id=request.user.id)
    followed_users_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)


    return render(request, 'users_view.html', {'users': users, "followed_users_ids": followed_users_ids})

@login_required(login_url='login')
def follow_user(request, pk):
    chosen_user = CustomUser.objects.get(id=pk)
    following = Follow.objects.create(
        follower=request.user,
        following=chosen_user
    )
    following.save()
    messages.success(request, f'You has been successfully followed {chosen_user.username}')
    
    return redirect('home')

@login_required(login_url='login')
def unfollow_user(request, pk):
    chosen_user = CustomUser.objects.get(id=pk)
    following = Follow.objects.get(follower=request.user, following=chosen_user)
    following.delete()

    messages.success(request, f'You has been successfully UNfollowed {chosen_user.username}')

    return redirect('home')

@login_required(login_url='login')
def liking_post_view(request, pk):
    result = [int(i) for i in pk if i.isdigit()][0]
    post = get_object_or_404(Post, id=result)
    user = request.user

    try:
        like = Like.objects.get(post=post, user=user)
    except:
        like = None

    if like:
        like.delete()
        count = Like.objects.filter(Q(user=request.user) and Q(post=post)).count()
        return JsonResponse(f'deleted {count}', safe=False)
    else:
        Like.objects.create(
            user=user,
            post=post
        )
        count = Like.objects.filter(Q(user=request.user) and Q(post=post)).count()
        return JsonResponse(f'created {count}', safe=False)

# @login_required(login_url='login')
# def un_liking_post_view(request, pk):
#     post = get_object_or_404(Post, id=pk)

#     if request.method == 'POST':
#         like_action = Like.objects.get(post=post, user=request.user)
#         like_action.delete()
#         # post.delete()
#         messages.success(request, 'You has been successfully Unlike this post')

#     return redirect('home')

@login_required(login_url='login')
def create_comment_view(request, pk):
    user = request.user
    target_post = Post.objects.get(id=pk)

    if request.method == 'POST':
        new_comment_text = request.POST.get('create_comment')
        new_comment = Comment.objects.create(
            user=user,
            post=target_post,
            text=new_comment_text,
        )

        new_comment.save()
        messages.success(request, 'You has been successfully created a comment on this post')

    return redirect('home')

@login_required(login_url='login')
def share_post_view(request, pk):
    user = request.user
    target_post = Post.objects.get(id=pk)

    print(target_post)

    Share.objects.create(
        user=user,
        post=target_post,
    )

    shares_count = Share.objects.filter(user=user,
        post=target_post).count()

    print(shares_count)
    # messages.success(request, 'You has been successfully Shared this post')

    return JsonResponse(f'works {shares_count}', safe=False)


def chat_view(request):
    users = CustomUser.objects.all().exclude(id=request.user.id)

    context = {
        'users': users,
    }
    return render(request, 'chat.html', context)


def send_message_view(request, pk):
    user = get_object_or_404(CustomUser, id=pk)        


    chats = Message.objects.filter(Q(sender=request.user, receiver=user.id) | Q(sender=user.id, receiver=request.user)).order_by('created_at')


    context = {
        'user': user,
        'chats': chats,
    }

    return render(request, 'send_message_view.html', context)


def create_message(request, pk):
    receiver = get_object_or_404(CustomUser, id=pk)
    sender = request.user
    body = json.loads(request.body)["messageText"]

    Message.objects.create(
        sender=sender,
        receiver=receiver,
        body=body,
    )

    return JsonResponse('Item was added', safe=False)

def get_messages_view(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    chats = Message.objects.filter(sender=user.id,  receiver=request.user)

    arr = []
    for chat in chats:
        arr.append(chat.body)
        

    return JsonResponse(arr, safe=False)