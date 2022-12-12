from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from dateutil import parser
from django import forms

from .models import TrackedBet


class NewTrackedBetForm(forms.ModelForm):
    class Meta:
        model = TrackedBet
        fields = [ 'sportsbook', 'sport', 'market', 'description', 'points', 'bet_amount', 'odds', 'winnings', 'result' ]
