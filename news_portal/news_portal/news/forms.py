from django import forms

from django.core.validators import ValidationError

from django.contrib.auth.models import Group

from allauth.account.forms import SignupForm
from django.urls import reverse

from .models import Post, Author, User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post_title', 'post_category', 'post_content']


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['author_bio']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

        def clean_email(self):
            email = self.cleaned_data.get('email')
            username = self.cleaned_data.get('username')
            if email and User.objects.filter(email=email).exclude(username=username).exists():
                raise forms.ValidationError('EMAIL NOT UNIQUE - USERNAME NOT UNIQUE')
            return email

        def get_absolute_url(self):
            return reverse('user_detail', kwargs={'pk': self.pk})


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


