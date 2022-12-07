import datetime
from django.conf import settings
from django.shortcuts import render
import pytz

from .models import Sport, Game, Bookmaker, BetOdds
from .odds_api import OddsAPI

def nfl_odds(request):
    sport = "americanfootball_nfl"
    books = "draftkings,fanduel"
    # Update sport odds every five minutes
    now = datetime.datetime.now(pytz.timezone("UTC"))
    if not Sport.objects.get(key=sport).last_update_time or Sport.objects.get(key=sport).last_update_time + datetime.timedelta(minutes=5) < now:
        api = OddsAPI(settings.ODDS_API_KEY)
        nfl_odds = api.get_odds(sport, books)
        add_odds_to_db(nfl_odds)
        Sport.objects.filter(key=sport).update(last_update_time=now)

    return render(request, "odds/odds.html")

def add_odds_to_db(game_odds):
    for game in game_odds:
        Game.objects.update_or_create(
            id=game["id"],
            defaults={
                "id": game["id"],
                "sport": Sport(key=game["sport_key"]),
                "commence_time": game["commence_time"],
                "home_team": game["home_team"],
                "away_team": game["away_team"],
            }
        )
        for bookmaker in game["bookmakers"]:
            for market in bookmaker["markets"]:
                BetOdds.objects.update_or_create(
                    game=Game(id=game["id"]),
                    bookmaker=Bookmaker(key=bookmaker["key"]),
                    market=market["key"],
                    defaults={
                        "game": Game(id=game["id"]),
                        "bookmaker": Bookmaker(key=bookmaker["key"]),
                        "market": market["key"],
                        "last_update_time": bookmaker["last_update"],
                        "name_1": market["outcomes"][0]["name"],
                        "price_1": market["outcomes"][0]["price"],
                        "name_2": market["outcomes"][1]["name"],
                        "price_2": market["outcomes"][1]["price"],
                        "point_1": market["outcomes"][0]["point"] if market["key"] != "h2h" else None,
                        "point_2": market["outcomes"][1]["point"] if market["key"] != "h2h" else None,
                    }
                )
