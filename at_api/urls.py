from django.urls import path
from . import views

# URL configureation
urlpatterns = [
    path(route="get_characters/", view=views.get_characters)
]