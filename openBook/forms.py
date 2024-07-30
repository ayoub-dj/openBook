from typing import Any, Mapping
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from users.models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from users.models import Post, Profile
from tinymce.widgets import TinyMCE

class CustomUserForm(forms.ModelForm):
    password1 = forms.CharField(max_length=120, widget=forms.PasswordInput(attrs={
        'Placeholder': 'New Password',
        'autocomplete': 'password',
        'class': 'form-control',
    }))
    password2 = forms.CharField(max_length=120, widget=forms.PasswordInput(attrs={
        'Placeholder': 'New Password Confirmation',
        'autocomplete': 'password',
        'class': 'form-control',
    }))

    class Meta:
        model = CustomUser
        fields = ('email', 'username')
        widgets = {
            'email': forms.EmailInput(attrs={'Placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'Placeholder': 'Username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = ''

class CustomProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'name', 'bio')
        widgets = {
            'name': forms.TextInput(attrs={'Placeholder': 'Full Name'}),
            'bio': forms.Textarea(attrs={'Placeholder': 'Bio'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = ''

class TinymceForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    
    class Meta:
        model = Post
        fields = ('text', )

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username',
        'autocomplete': 'username',
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'autocomplete': 'email',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'autocomplete': 'password1',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'autocomplete': 'password2',
    }))

        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password does not match")
        
        return password2
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = ''
    
    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password1'),
        )

        return user
    
class PasswordRecovery(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'autocomplete': 'email',
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email does not exists")
        
        return email
    
    def __init__(self, *args, **kwargs):
        super(PasswordRecovery, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = ''

class SetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New Password',
    }))

    def __init__(self, user, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.user = user

        for field_name in self.fields:
            self.fields[field_name].label = ''
            

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password'])
        if commit:
            self.user.save()
        return self.user




# class SignUpForm(UserCreationForm):

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2')

# class SignUpForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password',
#                                 widget=forms.PasswordInput(attrs={
#                                     'class': 'just-me',
#                                     'placeholder': 'Password',
#                                 }))
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
#         'class': 'just-me',
#         'placeholder': 'Confirm Password',
#     }))

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email')

#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')

#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
        
#         return password2
    
#     def __init__(self, *args, **kwargs):
#         super(SignUpForm, self).__init__(*args, **kwargs)

#         for field_name in self.fields:
#             self.fields[field_name].label = ''
    
#     def save(self, commit=True):
#         user = super(SignUpForm, self).save(commit=False)
#         user.set_password(self.cleaned_data.get('password1'))

#         if commit:
#             user.save()
        
#         return user
