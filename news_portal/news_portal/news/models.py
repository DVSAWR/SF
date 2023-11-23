from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce

from django.urls import reverse

from django.contrib.auth.models import User, Group

from allauth.account.forms import SignupForm


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    author_bio = models.CharField(max_length=300, blank=True)

    def update_rating(self):
        total_post_rating = Post.objects.filter(post_author=self).aggregate(
            tpr=Coalesce(Sum('post_rating'), 0))
        total_comments_rating = Comment.objects.filter(comment_author=self).aggregate(
            tcr=Coalesce(Sum('comment_rating'), 0))
        total_post_comments_rating = self.post_set.aggregate(
            tpcr=Coalesce(Sum('comment__comment_rating'), 0))

        self.user_rating = total_post_rating * 3 + total_comments_rating + total_post_comments_rating
        self.save()


class Post(models.Model):
    ARTICLE = 'ARL'
    NEWS = 'NWS'
    PT_CHOICES = [
        (ARTICLE, 'article'),
        (NEWS, 'news')
    ]

    post_type = models.CharField(max_length=3, choices=PT_CHOICES)
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_create_datetime = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField('Category', through='PostCategory')
    post_title = models.CharField(max_length=200)
    post_content = models.TextField(max_length=5000)
    post_rating = models.IntegerField(default=0)

    def preview(self):
        return self.post_content[:150] + '...'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.pk})


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    subscribers = models.ManyToManyField(User, related_name="categories", blank=True)

    def __str__(self):
        return self.category_name.title()


class PostCategory(models.Model):
    pc_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    pc_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=1000)
    comment_create_datetime = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


