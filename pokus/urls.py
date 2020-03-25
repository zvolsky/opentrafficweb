from django.urls import path, include
from .views import where

urlpatterns = [
    path('where/', where, name='where'),
]
