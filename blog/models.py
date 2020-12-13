from django.db import models


class Blog(models.Model):
    """
    Блог
    """
    owner = models.OneToOneField(verbose_name='Blog owner', to='auth.User', on_delete=models.CASCADE, related_name='blog')
    description = models.TextField(blank=True)
    created = models.DateTimeField('Date of creation', auto_now_add=True)
    updated = models.DateTimeField('Date of last update', auto_now=True, blank=True)

    def __str__(self):
        return f"Blog belongs to {self.owner.get_full_name()} (id: {self.owner_id})"