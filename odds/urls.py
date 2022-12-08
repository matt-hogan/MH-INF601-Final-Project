from django.urls import path

from . import views

app_name = "odds"
urlpatterns = [
    path("<str:sport>/", views.sport_odds, name="sport_odds"),
]