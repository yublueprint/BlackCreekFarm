from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import Livestock, Crop, Equipment
from app.logging.logging import Logger

# Initialize application logger (writes events to app/logging/app.log)
logger = Logger("app/logging/app.log")


@login_required
def dashboard(request):
    """
    Render the dashboard page with live data and recent activity.

    - Retrieves real-time counts of livestock, crops, and equipment.
    - Fetches recent activity from the custom Logger.
    - Logs when the current user views the dashboard.
    """

    # Log dashboard access for auditing / monitoring
    logger.log(f"User {request.user} viewed dashboard.")

    # NOTE:
    # Do NOT store these counts in separate variables outside of this function.
    # They must be retrieved inside the render() context to ensure values are updated
    # in real time whenever the dashboard is requested.
    context = {
        "livestock_count": Livestock.objects.count(),      # Count of all livestock records
        "crop_count": Crop.objects.count(),                # Count of all crop records
        "equipment_count": Equipment.objects.count(),      # Count of all equipment records
        "recent_activity": logger.retrieve_recent_activity # Recent user/system activity
    }

    # Render the dashboard template with the context data
    return render(request, "dashboard.html", context)

