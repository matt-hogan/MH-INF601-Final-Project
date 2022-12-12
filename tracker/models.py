from django.conf import settings
from django.db import models

from .validators import validate_bet_amount, validate_odds


class TrackedBet(models.Model):
    RESULT_CHOICES = (
        ('pending', 'Pending'),
        ('win', 'Win'),
        ('loss', 'Loss'),
        ('void', 'Void'),
    )
    MARKET_CHOICES = (
        ('h2h', 'Moneyline'),
        ('spreads', 'Spread'),
        ('totals', 'Total'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    sportsbook = models.CharField(max_length=50)
    sport = models.CharField(max_length=50)
    market = models.CharField(choices=MARKET_CHOICES, max_length=20, )
    description = models.CharField(max_length=240)
    points = models.FloatField(blank=True, null=True)
    bet_amount = models.FloatField(validators=[validate_bet_amount])
    odds = models.IntegerField(validators=[validate_odds])
    winnings = models.FloatField(blank=True, null=True) # For both potential and realized
    result = models.CharField(choices=RESULT_CHOICES, default='pending', max_length=20)

    REQUIRED_FIELDS = [ 'user', 'sportsbook', 'sport', 'market', 'description', 'bet_amount', 'odds', 'winnings', 'result' ]

