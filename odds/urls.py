from django.urls import path

from . import views

app_name = "odds"
urlpatterns = [
    path("nfl/", views.nfl_odds, name="nfl_odds"),
]