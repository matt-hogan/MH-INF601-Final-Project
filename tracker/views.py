from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import TrackedBetForm
from .models import TrackedBet


@login_required
def tracker(request):
    bets = TrackedBet.objects.filter(user=request.user).values()
    profit = get_profit(bets)
    context = {
        "df": bets,
        "add_form": TrackedBetForm(),
        "profit": "%.2f"%profit
    }
    return render(request, "tracker/tracker.html", context)


def get_profit(bets):
    """  """
    profit = 0
    for bet in bets:
        if bet["result"] == 'win':
            profit += bet["winnings"]
            profit += bet["bet_amount"]
        elif bet["result"] == 'loss':
            profit += bet["winnings"]
            profit += bet["bet_amount"]
    return profit


@login_required
def create_tracked_bet(request):
    """  """
    if request.POST:
        TrackedBet.objects.create(
            user=request.user,
            sportsbook=request.POST["sportsbook"],
            sport=request.POST["sport"],
            market=request.POST["market"],
            description=request.POST["description"],
            points=request.POST["points"],
            bet_amount=request.POST["bet_amount"],
            odds=request.POST["odds"],
            winnings=request.POST["winnings"],
            result=request.POST["result"],
        )
    return HttpResponseRedirect(reverse("tracker:track"))


@login_required
def update_tracked_bet(request, tracked_bet_id):
    if request.POST:
        TrackedBet.objects.filter(id=tracked_bet_id).update(
            sportsbook=request.POST["sportsbook"],
            sport=request.POST["sport"],
            market=request.POST["market"],
            description=request.POST["description"],
            points=request.POST["points"],
            bet_amount=request.POST["bet_amount"],
            odds=request.POST["odds"],
            winnings=request.POST["winnings"],
            result=request.POST["result"],
        )
        return HttpResponseRedirect(reverse("tracker:track"))
    bet = TrackedBet.objects.get(id=tracked_bet_id)
    context = {
        "form": TrackedBetForm(instance=bet),
        "bet_id": tracked_bet_id,
    }
    return render(request, "tracker/update.html", context)


@login_required
def delete_tracked_bet(request, tracked_bet_id):
    bet = get_object_or_404(TrackedBet, pk=tracked_bet_id)
    bet.delete()
    return HttpResponseRedirect(reverse("tracker:track"))

