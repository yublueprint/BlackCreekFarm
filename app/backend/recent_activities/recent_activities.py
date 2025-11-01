from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404

from app.logging.logging import Logger

logger = Logger("app/logging/app.log")

@login_required
def recent_activities_list(request):
    logger.log(f"User {request.user} viewed recent activities list.")

    context = {
        "recent_activities" : logger.retrieve_recent_activity(50, True),
    }

    return render(request, "app/recent_activities_list.html", context)