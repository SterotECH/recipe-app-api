"""
Serializer for recipe APIs
"""

from rest_framework import serializers

from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe"""

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'slug',
            'times_minutes',
            'price',
            'link',
            ]
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe details view.
    """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
