from django.contrib import admin

from .models import TrackedBet


@admin.register(TrackedBet)
class BetTrackerdAdmin(admin.ModelAdmin):
    fields = [ 'user', 'sportsbook', 'sport', 'market', 'description', 'points', 'bet_amount', 'odds', 'winnings', 'result' ]
    list_display = [ 'user', 'sportsbook', 'sport', 'market', 'description', 'points', 'bet_amount', 'odds', 'winnings', 'result' ]
