from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Rating


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'first_name')


class ProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('picture',)

class RatingForm(forms.ModelForm):
    class Meta():
        model = Rating
        fields = ('value', 'movie')
