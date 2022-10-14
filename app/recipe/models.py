"""
Database models= for recipe
"""
from django.db import models
from django.conf import settings


class Recipe(models.Model):
    """Recipe Object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    times_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']
