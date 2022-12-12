from django.urls import path

from . import views

app_name = "tracker"
urlpatterns = [
    path("tracker/", views.tracker, name="track"),
    path("tracker/add", views.create_tracked_bet, name="add_bet"),
    path("tracker/update/<int:tracked_bet_id>", views.update_tracked_bet, name="update_bet"),
    path("tracker/delete/<int:tracked_bet_id>", views.delete_tracked_bet, name="delete_bet"),
]