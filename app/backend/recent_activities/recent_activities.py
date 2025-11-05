from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.logging.logging import Logger

logger = Logger("app/logging/app.log")

@login_required
def recent_activities_list(request):
    logger.log(f"User {request.user} viewed recent activities list.")

    context = {
        "recent_activity": logger.retrieve_recent_activity(5, True),
    }

    return render(request, "app/recent_activities_list.html", context)