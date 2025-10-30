from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404

from app.logging.logging import Logger

logger = Logger("app/logging/app.log")

@login_required
def recent_activities_list(request):
    logger.log(f"User {request.user} viewed recent activities list.")

    context = {
        "recent_activities" : logger.retrieve_recent_activity(50),
        "next_offset" : 50,
    }

    return render(request, "app/recent_activities_list.html", context)

@login_required
def retrieve_more(request):
    logger.log(f"User {request.user} retrieved more recent activities.")

    return redirect("recent_activities_list")