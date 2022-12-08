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

    formatted_odds = format_odds_for_html(sport, now)
    context = {
        "odds": formatted_odds
    }
    return render(request, "odds/odds.html", context)


def add_odds_to_db(game_odds):
    """ Takes in a json response from the odds api and adds the odds to the database """
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


def format_odds_for_html(sport, now):
    """ Retrieves odds from the database for the given sport and returns them formatted for use in the html """
    odds = BetOdds.objects.select_related().filter(game__sport__key=sport, game__commence_time__gt=now)
    game_odds_list = []
    games_added = []
    # Combines all odds for a game into a single object
    for odd in odds:
        if odd.game.id in games_added:
            game_index = games_added.index(odd.game.id)
            game_markets = game_odds_list[game_index]["markets"]
            if odd.market not in game_markets.keys():
                game_markets[odd.market] = {}
            game_markets[odd.market][odd.bookmaker.title] = [
                {
                    "name": odd.name_1,
                    "price": odd.price_1,
                    "point": odd.point_1,
                },
                {
                    "name": odd.name_2,
                    "price": odd.price_2,
                    "point": odd.point_2,
                }
            ]
        else:
            games_added.append(odd.game.id)
            game_odds_list.append({
                "info": {
                    "id": odd.game.id,
                    "time": odd.game.commence_time,
                    "away_team": odd.game.away_team,
                    "home_team": odd.game.home_team,
                },
                "markets": {
                    odd.market: {
                        odd.bookmaker.title: [
                            {
                                "name": odd.name_1,
                                "price": odd.price_1,
                                "point": odd.point_1,
                            },
                            {
                                "name": odd.name_2,
                                "price": odd.price_2,
                                "point": odd.point_2,
                            }
                        ]
                    }
                }
            })
    # Calculate the best odds for game's markets
    for game in game_odds_list:
        for market, book_odds in game["markets"].items(): 
            best_odds = [{"name": None, "price": None, "point": None, "bookmaker": None}, {"name": None, "price": None, "point": None, "bookmaker": None}]
            for book, odds_list in book_odds.items():
                for odd, best_odd in zip(odds_list, best_odds):
                    if market == "h2h":
                        if not best_odd["price"] or odd["price"] > best_odd["price"]:
                            best_odd["name"] = odd["name"]
                            best_odd["price"] = odd["price"]
                            best_odd["bookmaker"] = book
                    elif market == "spreads":
                        if not best_odd["point"] or odd["point"] >= best_odd["point"]:
                            if not best_odd["price"] or odd["price"] > best_odd["price"]:
                                best_odd["name"] = odd["name"]
                                best_odd["price"] = odd["price"]
                                best_odd["point"] = odd["point"]
                                best_odd["bookmaker"] = book
                    elif market == "totals":
                        if odd["name"] == "Under":
                            if not best_odd["point"] or odd["point"] >= best_odd["point"]:
                                if not best_odd["price"] or odd["price"] > best_odd["price"]:
                                    best_odd["name"] = odd["name"]
                                    best_odd["price"] = odd["price"]
                                    best_odd["point"] = odd["point"]
                                    best_odd["bookmaker"] = book
                        elif odd["name"] == "Over":
                            if not best_odd["point"] or odd["point"] <= best_odd["point"]:
                                if not best_odd["price"] or odd["price"] > best_odd["price"]:
                                    best_odd["name"] = odd["name"]
                                    best_odd["price"] = odd["price"]
                                    best_odd["point"] = odd["point"]
                                    best_odd["bookmaker"] = book
            book_odds["Best"] = best_odds
    return game_odds_list