from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    date=DateFilter(field_name='date',widget=forms.DateInput(attrs={'type':'date'}), lookup_expr='date__gte')
    class Meta:
        model=Post
        fields={'title' : ['icontains'],
                'post_author__author_user__username':['icontains']

        }