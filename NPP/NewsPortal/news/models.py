from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(post_author=self).aggregate(result=Sum('rating')).get('result')
        comments_rating = Comment.objects.filter(user_comment=self.author_user).aggregate(result=Sum('rating')).get(
            'result')
        comment_post = Comment.objects.filter(post_comment__post_author__author_user=self.author_user).aggregate(
            result=Sum('rating')).get('result')

        self.rating = (posts_rating * 3 + comments_rating + comment_post)
        self.save()



class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=255)
    subscribers = models.ManyToManyField(User, related_name="categories",blank=True)
    def __str__(self):
        return self.category_name.title()


class Post(models.Model):
    CHOICES = [
        ('post', 'Статья'),
        ('news', 'Новость'),
    ]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    category_post = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + "..."
    def get_absolute_url(self):
        return reverse('post_list')


class PostCategory(models.Model):
    post_category = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_post = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.post_category.name


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()