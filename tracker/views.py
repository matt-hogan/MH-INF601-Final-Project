from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView
import pandas as pd

from .forms import NewTrackedBetForm
from .models import TrackedBet


@login_required
def tracker(request):
    # Dispaly all tracked bet with filters
    # Display earnings

    bets = TrackedBet.objects.filter(user=request.user).values()
    bets_df = pd.DataFrame(bets)
    # TODO: format before displaying
    context = {
        "df": bets,
        "add_form": NewTrackedBetForm()
    }
    return render(request, "tracker/tracker.html", context)

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
            winnings=request.POST["bet_amount"],
            result=request.POST["result"],
        )
    return HttpResponseRedirect(reverse("tracker:track"))

@login_required
def update_tracked_bet(request, tracked_bet_id):
    TrackedBet.objects.filter(id=tracked_bet_id).update(
        sportsbook=request.POST["sportsbook"],
        sport=request.POST["sport"],
        market=request.POST["market"],
        description=request.POST["description"],
        points=request.POST["points"],
        bet_amount=request.POST["bet_amount"],
        odds=request.POST["odds"],
        winnings=request.POST["bet_amount"],
        result=request.POST["result"],
    )
    return HttpResponseRedirect(reverse("tracker:track"))

@login_required
def delete_tracked_bet(request, tracked_bet_id):
    bet = get_object_or_404(TrackedBet, pk=tracked_bet_id)
    bet.delete()
    return HttpResponseRedirect(reverse("tracker:track"))

