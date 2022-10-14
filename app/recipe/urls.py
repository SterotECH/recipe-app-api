"""
Recipes Mapping For the recipes App
"""

from rest_framework.routers import DefaultRouter

from recipe import views

app_name = 'recipe'
router = DefaultRouter()

router.register('', views.RecipeViewSet, basename='recipe')

urlpatterns = router.urls
