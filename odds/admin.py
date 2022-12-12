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
    fields = [ "id", "commence_time", "home_team", "away_team" ]
    list_display = ( "id", "sport", "commence_time", "home_team", "away_team" )

@admin.register(BetOdds)
class BetOddsAdmin(admin.ModelAdmin):
    # fields = [ "market", "name_1", "price_1", "point_1", "name_2", "price_2", "point_2", "last_update_time" ]
    list_display = [
        "get_sport",
        "get_game",
        "get_bookmaker",
        "market",
        "name_1",
        "price_1",
        "point_1",
        "name_2",
        "price_2",
        "point_2",
        "last_update_time"
    ]

    def get_game(self, obj):
        return obj.game

    def get_bookmaker(self, obj):
        return obj.bookmaker.title

    def get_sport(self, obj):
        return obj.game.sport.title
