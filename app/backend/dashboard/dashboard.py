import gc

import httpx
from asgiref.sync import sync_to_async
from django.contrib import messages
from django.shortcuts import redirect, render

from app.logging.logging import Logger

from ..models import Alert, Crop, Equipment, Livestock

# Initialize application logger
logger = Logger("app/logging/app.log")


async def dashboard(request):
    """
    Render the dashboard page with live data and recent activity.
    """

    try:
        user = await request.auser()

        livestock_growth = 0
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "http://localhost:8080/api/metrics/livestock/growth", timeout=1.0
                )
                if response.status_code == 200:
                    livestock_growth = response.json().get("growth_percentage", 0)
            except Exception as e:
                await sync_to_async(logger.log)(f"Failed to fetch growth metrics: {e}")

        alerts_queryset = Alert.objects.filter(is_read=False).order_by("-timestamp")[:5]
        recent_alerts = [alert async for alert in alerts_queryset]

        context = {
            "livestock_count": await Livestock.objects.acount(),
            "livestock_growth": livestock_growth,
            "crop_count": await Crop.objects.acount(),
            "equipment_count": await Equipment.objects.acount(),
            "recent_activity": await sync_to_async(logger.retrieve_recent_activity)(
                amount_to_retrieve=5
            ),
            "recent_alerts": recent_alerts,
        }

        gc.collect()

        await sync_to_async(logger.log)(f"User {user} viewed dashboard.")
        return render(request, "dashboard.html", context)
    except Exception as e:
        logger.log(f"Error in dashboard view by {request.user}: {e}")
        messages.error(request, str(e))
        return redirect("error_page")
