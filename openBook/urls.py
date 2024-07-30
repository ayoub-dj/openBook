"""
URL configuration for openBook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as home_views
from . import views_clb as home_class_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),

    path('accounts/', include('allauth.urls')),

    path('password_recovery/<uuidb64>/<token>/', home_views.password_recovery_view, name='password_recovery'),

    path('activate_email/<uuidb64>/<token>/', home_views.activate_email, name='activate_email'),

    # Authentication
    path('', home_views.home_view, name='home'),
    # path('', home_class_views.CustomHomeView.as_view(), name='home'),
    path('login/', home_views.login_view, name='login'),
    # path('login/', home_class_views.CustomLoginView.as_view(), name='login'),
    path('logout/', home_views.logout_view, name='logout'),
    # path('logout/', home_class_views.CustomLogoutView.as_view(), name='logout'),
    path('register/', home_views.register_view, name='register'),
    # path('register/', home_class_views.CustomRegisterView.as_view(), name='register'),


    path('password/recovery/email/', home_views.password_recovery_email_view, name='password_recovery_email'),
    # path('password/recovery/email/', home_class_views.PasswordRecoveryEmailView.as_view(), name='password_recovery_email'),




    # Posts
    path('delete-post/<pk>/', home_views.delete_post_view, name='delete-post'),
    # path('delete-post/<pk>/', home_class_views.DeletePostView.as_view(), name='delete-post'),
    path('edit-post/<pk>/', home_views.edit_post_view, name='edit-post'),
    # path('edit-post/<pk>/', home_class_views.EditPostView.as_view(), name='edit-post'),



    # Settings
    path('settings/<pk>/', home_views.settings_view, name='settings'),
    # path('settings/<pk>/', home_class_views.SettingsView.as_view(), name='settings'),
    path('settings/update-profile/<str:pk>/', home_views.update_profile_view, name='update_profile'),
    # path('settings/update-profile/<str:pk>/', home_class_views.UpdateProfileView.as_view(), name='update_profile'),
    path('settings/update-user/<str:pk>/', home_views.update_user_view, name='update_user'),



    # Profiles
    path('complete-profile/', home_views.complete_profile_view, name='complete_profile'),
    # path('complete-profile/', home_class_views.CompleteProfileView.as_view(), name='complete_profile'),
    path('profile/', home_views.profile_view, name='profile'),
    # path('profile/', home_class_views.ProfileView.as_view(), name='profile'),
    path('users/', home_views.users_view, name='users'),
    # path('users/', home_class_views.UserView.as_view(), name='users'),



    # Followers
    path('follow_user/<pk>/', home_views.follow_user, name='follow_user'),
    # path('follow_user/<pk>/', home_class_views.FollowUserView.as_view(), name='follow_user'),
    path('unfollow_user/<pk>/', home_views.unfollow_user, name='unfollow_user'),
    # path('unfollow_user/<pk>/', home_class_views.UnFollowUserView.as_view(), name='unfollow_user'),



    # Likes
    path('liking/<pk>/', home_views.liking_post_view, name='liking_post'),
    # path('liking/<pk>/', home_class_views.LikingPostView.as_view(), name='liking_post'),

    
    # path('unliking/<pk>/', home_views.un_liking_post_view, name='un_liking_post'),
    # path('unliking/<pk>/', home_class_views.UnLikingPostView.as_view(), name='un_liking_post'),



    # Comments
    path('create-comment/<pk>/', home_views.create_comment_view, name='create_comment_view'),
    # path('create-comment/<pk>/', home_class_views.CreateCommentView.as_view(), name='create_comment_view'),

    # Shares
    path('share-post/<pk>/', home_views.share_post_view, name='share_post_view'),
    # path('share-post/<pk>/', home_class_views.SharePostView.as_view(), name='share_post_view'),

    path('chat/', home_views.chat_view, name='chat_view'),

    path('send_message_view/<pk>', home_views.send_message_view, name='send_message_view'),

    path('create_message/<pk>', home_views.create_message, name='create_message'),
    path('get_messages/<pk>', home_views.get_messages_view, name='get_messages_view'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
