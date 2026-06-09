import gc

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.logging.logging import Logger

from ..models import Alert, Crop, Equipment, Livestock

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

    # Fetch growth metrics from Analytics Engine
    livestock_growth = 0
    try:
        response = requests.get(
            "http://localhost:8080/api/metrics/livestock/growth", timeout=1
        )
        if response.status_code == 200:
            livestock_growth = response.json().get("growth_percentage", 0)
    except Exception as e:
        logger.log(f"Failed to fetch growth metrics: {e}")

    # Fetch recent unread alerts
    recent_alerts = Alert.objects.filter(is_read=False).order_by("-timestamp")[:5]

    context = {
        "livestock_count": Livestock.objects.count(),  # Count of all livestock records
        "livestock_growth": livestock_growth,
        "crop_count": Crop.objects.count(),  # Count of all crop records
        "equipment_count": Equipment.objects.count(),  # Count of all equipment records
        "recent_activity": logger.retrieve_recent_activity(),  # Recent user/system activity
        "recent_alerts": recent_alerts,
    }

    gc.collect()

    # Render the dashboard template with the context data
    return render(request, "dashboard.html", context)
