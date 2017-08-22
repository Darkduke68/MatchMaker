from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from matches.models import Match


@login_required()
def dashboard(request):
    """Endpoint to view user matches. """

    matches = Match.objects.get_matches_with_percent(request.user)[:8]
    print(matches)
    context = {
        "matches": matches,
    }
    return render(request, "dashboards/main.html", context)
