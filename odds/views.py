import datetime
from django.conf import settings
from django.shortcuts import render

from .models import Sport, Game, Bookmaker, GameOdds, Outcome
from .odds_api import OddsAPI

def nfl_odds(request):
    api = OddsAPI(settings.ODDS_API_KEY)
    nfl_odds = api.get_odds("americanfootball_nfl", "draftkings,fanduel")
    add_odds_to_db(nfl_odds)

    return render(request, "odds/odds.html")

def add_odds_to_db(game_odds):
    # Sport and bookmakers should already be added by default
    # Update sport odds every five minutes
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
            GameOdds.objects.update_or_create(
                game=Game(id=game["id"]),
                bookmaker=Bookmaker(key=bookmaker["key"]),
                defaults={
                    "game": Game(id=game["id"]),
                    "bookmaker": Bookmaker(key=bookmaker["key"]),
                    "last_update_time": bookmaker["last_update"], 
                }
            )
            for market in bookmaker["markets"]:
                Outcome.objects.update_or_create(
                    book_game=GameOdds.objects.get(
                        game=Game(id=game["id"]),
                        bookmaker=Bookmaker(key=bookmaker["key"])
                    ),
                    market=market["key"],
                    defaults={
                        "book_game": GameOdds.objects.get(
                            game=Game(id=game["id"]),
                            bookmaker=Bookmaker(key=bookmaker["key"])
                        ),
                        "market": market["key"],
                        "name_1": market["outcomes"][0]["name"],
                        "price_1": market["outcomes"][0]["price"],
                        "name_2": market["outcomes"][1]["name"],
                        "price_2": market["outcomes"][1]["price"],
                        "point_1": market["outcomes"][0]["point"] if market["key"] != "h2h" else None,
                        "point_2": market["outcomes"][1]["point"] if market["key"] != "h2h" else None,
                    }
                )

# *** DEFAULTS ***
# import datetime
# from odds.models import Sport, Bookmaker
# Sport.objects.create(key="americanfootball_nfl", title="NFL", last_update_time=datetime.datetime.utcnow())
# Bookmaker.objects.bulk_create([
#     Bookmaker(key="draftkings", title="DraftKings"),
#     Bookmaker(key="fanduel", title="FanDuel")
# ])