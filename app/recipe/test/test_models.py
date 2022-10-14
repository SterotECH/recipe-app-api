from decimal import Decimal
from django.contrib.auth import get_user_model
from recipe import models


def test_create_recipe(self):
    """Testing a recipe is successful"""
    user = get_user_model().objects.create_user(
        email="test@domain.com",
        password='goodPass'
        )
    recipe = models.Recipe.objects.create(
        user=user,
        title="Sample recipe",
        slug="sample-recipe",
        time_minutes=5,
        price=Decimal('5.50'),
        description='Sample recipe description'
    )
    self.assertEqual(str(recipe), recipe.title)
