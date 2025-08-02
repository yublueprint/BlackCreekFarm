from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from app.logging.logging import Logger

from ..models import Livestock

logger = Logger("app/logging/app.log")


@login_required
def reports(request):
    try:
        livestock = Livestock.objects.all()
        logger.log(f"User {request.user} viewed livestock report.")
        return render(request, "app/reports.html", {"livestock": livestock})
    except Exception as e:
        logger.log(f"Error in reports view: {e}")
        return render(request, "app/error.html", {"error": "Failed to retrieve livestock data"})