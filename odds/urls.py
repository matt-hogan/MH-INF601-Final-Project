from django.urls import path

from . import views

app_name = "odds"
urlpatterns = [
    path("", views.odds_home, name="odds_home"),
    path("<str:sport>/", views.sport_odds, name="sport_odds"),
]