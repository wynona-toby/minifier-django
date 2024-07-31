# minifier/urls.py
from django.urls import path
from .views import MinifyView
# from . import views
urlpatterns = [
    path('minify/', MinifyView.as_view(), name='minify'),
]
