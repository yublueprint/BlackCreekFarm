from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import (Livestock, Crop, Equipment)
from app.logging.logging import Logger

# DO NOT USE INDIVIDUAL VARIABLES FOR THIS, MUST BE IN THE RENDER FUNCTION OR ELSE IT WONT UPDATE REAL TIME.
# livestock_count = Livestock.objects.count()
# crop_count = Crop.objects.count()
# equipment_count = Equipment.objects.count()
# recent_activity = logger.retrieve_recent_activity

logger = Logger("app/logging/app.log")

@login_required
def dashboard(request):
    logger.log(f"User {request.user} viewed dashboard.")
    return render(request, "dashboard.html", {"livestock_count": Livestock.objects.count(), "crop_count":Crop.objects.count(), "equipment_count": Equipment.objects.count(), "recent_activity": logger.retrieve_recent_activity})
