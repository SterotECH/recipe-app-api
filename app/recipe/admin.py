"""
Admiin Customization for the Recipe Admin
"""
from django.contrib import admin

from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin Customization for the recipe model"""
    autocomplete_fields = ['user']
    prepopulated_fields = {'slug': ['title']}
    list_filter = ['user', 'times_minutes', 'price']
    list_display = ['user', 'title', 'price']
    list_per_page: int = 10
    list_select_related = ['user']
    search_fields = ["user", "title"]
