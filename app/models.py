import uuid

from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
#https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
class Tag(models.Model):
    title = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + str(self.created_at)

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500)
    replies = models.ForeignKey(
        to='Comment',
        null=True,
        blank = True,
        related_name='comments',
        on_delete=models.SET_NULL
    )
    likes = models.ForeignKey(Like, related_name='comments', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.user) + self.text

class Post(models.Model):
    #alternative to uuid --> https://hashids.org/python/
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='posts', null=True, on_delete=models.SET_NULL)
    #auto_now --> whenever object is saved, auto_now_add --> only when object is 1st time created
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='posts')
    description = models.TextField(max_length=500)
    likes = models.ForeignKey(Like, related_name='posts', null=True, blank=True, on_delete=models.SET_NULL)
    comments = models.ForeignKey(Comment, related_name='posts', null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, through='Post_Tag', blank=True, null=True)

    def __str__(self):
        return str(self.user) + self.description

    '''
    def get_absolute_url(self):
        #<identifier>/<uuid>/
        return reverse('app:profile', kwargs={
            'identifier': self.user.identifier,
            'uuid': self.uuid
        })
    '''    
    class Meta:
        ordering = ["-created_at"]

class Post_Tag(models.Model):
    tag = models.ForeignKey(Tag, related_name='post_tag', null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, related_name='post_tag', null=True, on_delete=models.SET_NULL)
