from django.db import models

class Sport(models.Model):
    key = models.CharField(primary_key=True, max_length=50, unique=True)
    title = models.CharField(max_length=50, unique=True)
    last_update_time = models.DateTimeField()

class Game(models.Model):
    id = models.CharField(primary_key=True, max_length=50, unique=True)
    sport = models.ForeignKey(Sport, on_delete=models.DO_NOTHING, null=True, blank=True)
    commence_time = models.DateTimeField()
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)

class Bookmaker(models.Model):
    key = models.CharField(primary_key=True, max_length=50, unique=True)
    title = models.CharField(max_length=50, unique=True)

class GameOdds(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, null=True, blank=True)
    bookmaker = models.ForeignKey(Bookmaker, on_delete=models.DO_NOTHING, null=True, blank=True)
    last_update_time = models.DateTimeField()

class Outcome(models.Model):
    book_game = models.ForeignKey(GameOdds, on_delete=models.DO_NOTHING, null=True, blank=True)
    market = models.CharField(max_length=50)
    name_1 = models.CharField(max_length=50)
    price_1 = models.SmallIntegerField()
    point_1 = models.FloatField(blank=True, null=True)
    name_2 = models.CharField(max_length=50)
    price_2 = models.SmallIntegerField()
    point_2 = models.FloatField(blank=True, null=True)
