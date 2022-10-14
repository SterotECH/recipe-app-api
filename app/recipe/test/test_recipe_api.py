"""
Test for recipe APIs
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.models import Recipe
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id: Recipe):
    """Create and return a recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    """Create and return a new recipe object"""
    defaults = {
        'title': 'Sample Recipe',
        'slug': 'sample-recipe',
        'times_minutes': 22,
        'price': Decimal('20.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


def create_user(**params):
    """Create and return new User"""
    return get_user_model().objects.create_user(**params)  # type: ignore


class PublicApiTest(TestCase):
    """Test unauthenticated API request"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test authenticated API request"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(  # type: ignore
            email='test@domain.com',
            password='goodPass',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)  # type: ignore

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user"""
        other_user = create_user(
            email='test1@domain.com',
            password='goodPassOther'
            )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)   # type: ignore

    def test_get_recipe_details(self):
        """Test get recipe details."""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe_id=recipe.id)  # type: ignore
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)  # type: ignore

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
            'title': 'Sample title',
            'slug': 'sample-title',
            'times_minutes': 30,
            'price': Decimal('30.00')
        }
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])  # type: ignore
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Test partial Update of a recipe"""
        original_link = 'https://example.com/recipe.pdf'
        original_slug = 'sample-recipe-title'
        recipe = create_recipe(
            user=self.user,
            title='Sample Recipe title',
            link=original_link,
            slug=original_slug,
        )

        payload = {'title': 'new_recipe_title'}
        url = detail_url(recipe_id=recipe.id)  # type: ignore
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.slug, original_slug)
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """Test full update of a recipe"""
        recipe = create_recipe(
            user=self.user,
            title='Sample Recipe title',
            link='https://example.com/recipe.pdf',
            slug='sample-recipe-title',
            description='sample recipe description',
        )

        payload = {
            'title': 'new recipe title',
            'slug': 'new-recipe-title',
            'description': 'new sample description',
            'times_minutes': 10,
            'price': Decimal('2.50'),
            'link': 'http://example.com/new_recipe.pdf'
        }

        url = detail_url(recipe_id=recipe.id)  # type: ignore
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_return_error(self):
        """Test changing the recipe user results in an error"""
        new_user = create_user(email='user_2@domain.com', password='goodPass')
        recipe = create_recipe(user=new_user)

        payload = {'user': self.user.id}
        url = detail_url(recipe.id)  # type: ignore
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, new_user)

    def test_delete_recipe(self):
        """Test deleting recipe successfully"""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe_id=recipe.id)  # type: ignore
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Recipe.objects
            .filter(id=recipe.id)  # type: ignore
            .exists()
            )

    def test_delete_other_users_recipe_error(self):
        """Test trying to delete another users recipe gives error"""
        new_user = create_user(email='user_2@domain.com', password='goodPass')
        recipe = create_recipe(user=new_user)

        url = detail_url(recipe_id=recipe.id)  # type: ignore
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe
                        .objects
                        .filter(id=recipe.id)  # type: ignore
                        .exists()
                        )
