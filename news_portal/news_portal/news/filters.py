from django import forms
from django_filters import FilterSet, DateFilter

from .models import Post


class PostFilter(FilterSet):
    date = DateFilter(field_name='post_create_datetime', widget=forms.DateInput(attrs={'type': 'date'}),
                      lookup_expr='date__gte', label='Date is equal or greater then')

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'post_author__author_user__username': ['icontains'],
            # 'post_category__category_name': ['icontains']
        }

