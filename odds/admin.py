from django.contrib import admin

from .models import Sport, Game, Bookmaker, GameOdds, Outcome

class SportAdmin(admin.ModelAdmin):
    fields = [ "key", "title", "last_update_time" ]
    list_display = ( "key", "title", "last_update_time" )

class BookmakerAdmin(admin.ModelAdmin):
    fields = [ "key", "title" ]
    list_display = ( "key", "title" )

class GameAdmin(admin.ModelAdmin):
    fields = [ "id", "commence_time", "home_team", "away_team" ]
    list_display = ( "id", "sport", "commence_time", "home_team", "away_team" )

# class GameOddsAdmin(admin.ModelAdmin):
#     # fields = [ "game", "bookmaker", "commence_time", "home_team", "away_team" ]
#     list_display = ( "id", "sport", "commence_time", "home_team", "away_team" )

class OutcomeAdmin(admin.ModelAdmin):
    fields = [ "market", "name_1", "price_1", "point_1", "name_2", "price_2", "point_2" ]
    list_display = ( "market", "name_1", "price_1", "point_1", "name_2", "price_2", "point_2" )


admin.site.register(Sport, SportAdmin)
admin.site.register(Bookmaker, BookmakerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Outcome, OutcomeAdmin)