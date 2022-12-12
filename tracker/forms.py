from django import forms

from .models import TrackedBet


class TrackedBetForm(forms.ModelForm):
    class Meta:
        model = TrackedBet
        fields = [ 'sportsbook', 'sport', 'market', 'description', 'points', 'bet_amount', 'odds', 'winnings', 'result' ]
