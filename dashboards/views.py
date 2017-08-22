from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from matches.models import Match


@login_required()
def dashboard(request):
    """Endpoint to view user matches. """
    total_user_cnt = User.objects.all().count() - 1
    matches = Match.objects.get_matches_with_percent(request.user)[:8]
    print(matches)
    context = {
        "matches": matches,
        "total_user_cnt": total_user_cnt,
    }
    return render(request, "dashboards/main.html", context)
