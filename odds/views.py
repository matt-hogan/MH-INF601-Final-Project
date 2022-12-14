import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import pytz

from .models import Sport, Game, Bookmaker, BetOdds
from .odds_api import OddsAPI
from users.models import CustomUser


def odds_home(request):
    """ Main home page for the entire website """
    context = {
        "sports": Sport.objects.get_queryset()
    }
    return render(request, "home.html", context)


@login_required
def sport_odds(request, sport):
    """ Displays all upcoming games and best odds for the provided sport """
    sport_object = get_object_or_404(Sport, title=sport.upper())
    sport_key = sport_object.key
    books = CustomUser.objects.filter(email=request.user.email)[0].bookmakers
    # Update sport odds every five minutes
    now = datetime.datetime.now(pytz.timezone("UTC"))
    if not Sport.objects.get(key=sport_key).last_update_time or Sport.objects.get(key=sport_key).last_update_time + datetime.timedelta(minutes=5) < now:
        api = OddsAPI(settings.ODDS_API_KEY)
        odds = api.get_odds(sport_key, books)
        add_odds_to_db(odds)
        Sport.objects.filter(key=sport_key).update(last_update_time=now)

    formatted_odds = format_odds_for_html(sport_key, now, books)
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


def format_odds_for_html(sport, now, books):
    """ Retrieves odds from the database for the given sport and returns them formatted for use in the html """
    # Filters out games that have already been started or commpleted
    books_list = books.split(",")
    odds = BetOdds.objects.select_related().filter(game__sport__key=sport, game__commence_time__gt=now, bookmaker__key__in=books_list)
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
            # Stores the best odds from each market for each game
            if "Best" not in game_markets[odd.market].keys():
                game_markets[odd.market]["Best"] = [
                    {
                        "name": odd.name_1,
                        "price": odd.price_1,
                        "point": odd.point_1,
                        "bookmaker": odd.bookmaker.title,
                    },
                    {
                        "name": odd.name_2,
                        "price": odd.price_2,
                        "point": odd.point_2,
                        "bookmaker": odd.bookmaker.title,
                    }
                ]
            else:
                # Check if best odds can be updated
                best_odds = game_markets[odd.market]["Best"]
                current_odds = [{"name": odd.name_1, "price": odd.price_1, "point": odd.point_1}, {"name": odd.name_2, "price": odd.price_2, "point": odd.point_2}]
                for best_odd, current_odd in zip(best_odds, current_odds):
                    if odd.market == "h2h" or odd.market == "spreads" or (odd.market == "totals" and current_odd["name"] == "Under"):
                        if not best_odd["point"] or current_odd["point"] >= best_odd["point"]:
                            if not best_odd["price"] or current_odd["price"] > best_odd["price"]:
                                best_odd["name"] = current_odd["name"]
                                best_odd["price"] = current_odd["price"]
                                best_odd["point"] = current_odd["point"]
                                best_odd["bookmaker"] = odd.bookmaker.title
                    elif odd.market == "totals" and current_odd["name"] == "Over":
                        if not best_odd["point"] or current_odd["point"] <= best_odd["point"]:
                            if not best_odd["price"] or current_odd["price"] > best_odd["price"]:
                                best_odd["name"] = current_odd["name"]
                                best_odd["price"] = current_odd["price"]
                                best_odd["point"] = current_odd["point"]
                                best_odd["bookmaker"] = odd.bookmaker.title
        else:
            # Add new games and odds
            games_added.append(odd.game.id)
            game_odds_list.append({
                "info": {
                    "id": odd.game.id,
                    "time": odd.game.commence_time.astimezone(pytz.timezone('US/Eastern')),
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
                        ],
                        "Best": [
                            {
                                "name": odd.name_1,
                                "price": odd.price_1,
                                "point": odd.point_1,
                                "bookmaker": odd.bookmaker.title,
                            },
                            {
                                "name": odd.name_2,
                                "price": odd.price_2,
                                "point": odd.point_2,
                                "bookmaker": odd.bookmaker.title,
                            }
                        ],
                    }
                }
            })
    return game_odds_list