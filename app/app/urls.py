"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include


# Text to put at the end of each page's <title>.
site_title = "Recipe Api"

# Text to put in each page's <h1>.
site_header = "Recipe"

# Text to put at the top of the admin index page.
index_title = "admin"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("_/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "_/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("_/auth/user/", include("core.urls")),
    path('_/recipe/', include('recipe.urls')),
]
