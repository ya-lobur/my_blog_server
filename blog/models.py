from datetime import date

from django.db import models
from django.contrib.postgres.fields import ArrayField

from my_blog_server import settings


def get_post_media_path(instance, filename):
    today = date.today()
    return f'posts/profile/{instance.author.pk}/{today.year}/{today.month}/{today.day}/{filename}'


class Blog(models.Model):
    owner = models.OneToOneField(verbose_name='Blog owner', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog')
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField('Date of creation', auto_now_add=True)
    updated = models.DateTimeField('Date of last update', auto_now=True, blank=True)

    def __str__(self):
        return f"Blog pk: {self.pk} (owner pk: {self.owner_id})"


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    text_content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=get_post_media_path, blank=True, null=True)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    liked_by = ArrayField(models.PositiveIntegerField(), default=list)
    created = models.DateTimeField('Date of creation', auto_now_add=True)
    updated = models.DateTimeField('Date of last update', auto_now=True, blank=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        try:
            stored_post = self.__class__.objects.get(pk=self.pk)
            if stored_post.image != self.image:
                stored_post.image.delete(save=False)
        except self.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post: {self.pk} from blog {self.blog.pk} by {self.author_id}"
