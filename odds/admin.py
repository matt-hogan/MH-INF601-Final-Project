from django.contrib import admin

from .models import Sport, Game, Bookmaker, BetOdds

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    fields = [ "key", "title", "last_update_time" ]
    list_display = ( "key", "title", "last_update_time" )

@admin.register(Bookmaker)
class BookmakerAdmin(admin.ModelAdmin):
    fields = [ "key", "title" ]
    list_display = ( "key", "title" )

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    fields = [ "commence_time", "home_team", "away_team" ]
    list_display = ( "sport", "commence_time", "home_team", "away_team" )

@admin.register(BetOdds)
class BetOddsAdmin(admin.ModelAdmin):
    list_display = [
        "get_sport",
        "game",
        "bookmaker",
        "market",
        "name_1",
        "price_1",
        "point_1",
        "name_2",
        "price_2",
        "point_2",
        "last_update_time"
    ]

    def get_sport(self, obj):
        return obj.game.sport.title
