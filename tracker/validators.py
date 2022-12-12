from django.core.exceptions import ValidationError


""" Used for validating inputs to the database """

def validate_bet_amount(value):
    if value <= 0:
        raise ValidationError("Bet amount must be greater than 0")


def validate_odds(value):
    if value < 100 and value >=-100:
        raise ValidationError("Odds must be valid american odds")
