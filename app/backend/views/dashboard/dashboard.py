import httpx
from django.contrib import messages
from django.shortcuts import redirect, render

from app.logging.logging import Logger

from ...models import Alert, Crop, Equipment, Livestock

# Initialize application logger
logger = Logger("app/logging/app.log")

def dashboard(request):
    """
    Render the dashboard page with live data and recent activity.
    """
    try:
        user = request.user

        livestock_growth = 0
        with httpx.Client() as client:
            try:
                response = client.get(
                    "http://localhost:8080/api/metrics/livestock/growth", timeout=1.0
                )
                if response.status_code == 200:
                    livestock_growth = response.json().get("growth_percentage", 0)
            except Exception as e:
                logger.log(f"Failed to fetch growth metrics: {e}")

        recent_alerts = list(Alert.objects.filter(is_read=False).order_by("-timestamp")[:5])

        context = {
            "livestock_count": Livestock.objects.count(),
            "livestock_growth": livestock_growth,
            "crop_count": Crop.objects.count(),
            "equipment_count": Equipment.objects.count(),
            "recent_activity": logger.retrieve_recent_activity(amount_to_retrieve=5),
            "recent_alerts": recent_alerts,
        }

        logger.log(f"User {user} viewed dashboard.")
        return render(request, "dashboard.html", context)

    except Exception as e:
        logger.log(f"Error in dashboard view by {request.user}: {e}")
        messages.error(request, str(e))
        return redirect("error_page")