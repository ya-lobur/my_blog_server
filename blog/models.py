from django.db import models
from django.contrib.postgres.fields import ArrayField

from my_blog_server import settings


class Blog(models.Model):
    owner = models.OneToOneField(verbose_name='Blog owner', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog')
    description = models.TextField(blank=True)
    created = models.DateTimeField('Date of creation', auto_now_add=True)
    updated = models.DateTimeField('Date of last update', auto_now=True, blank=True)

    def __str__(self):
        return f"Blog pk: {self.pk} (owner pk: {self.owner_id})"


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    text_content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    liked_by = ArrayField(models.PositiveIntegerField(), default=list)
    created = models.DateTimeField('Date of creation', auto_now_add=True)
    updated = models.DateTimeField('Date of last update', auto_now=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Post: {self.pk} from blog {self.blog.pk} by {self.author_id}"
