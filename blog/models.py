from django.db import models
from django.contrib.postgres.fields import ArrayField


class Blog(models.Model):
    owner = models.OneToOneField(verbose_name='Blog owner', to='auth.User', on_delete=models.CASCADE, related_name='blog')
    description = models.TextField(blank=True)
    created = models.DateTimeField('Date of creation', auto_now_add=True)
    updated = models.DateTimeField('Date of last update', auto_now=True, blank=True)

    def __str__(self):
        return f"Blog belongs to {self.owner.get_full_name()} (id: {self.owner_id})"


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    text_content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(to='auth.User', on_delete=models.CASCADE, related_name='posts')
    liked_by = ArrayField(models.PositiveIntegerField(), default=list)
    created = models.DateTimeField('Date of creation', auto_now_add=True)
    updated = models.DateTimeField('Date of last update', auto_now=True, blank=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return f"Post(id: {self.pk}) from blog(id: {self.blog.pk}) by {self.author.get_full_name()}"
