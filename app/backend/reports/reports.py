import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from app.logging.logging import Logger

from ..models import Livestock

logger = Logger("app/logging/app.log")


@login_required
def reports(request):
    try:
        livestock = Livestock.objects.all()
        logger.log(f"User {request.user} viewed livestock reports page.")
        return render(request, "app/reports.html", {"livestock": livestock})
    except Exception as e:
        logger.log(f"Error in reports view by {request.user}: {e}")
        messages.error(request, str(e))
        return redirect("error_page")


@login_required
def download_livestock_report(request):
    logger.log(f"User {request.user} requested livestock PDF report.")
    try:
        # Proxy request to Spring Boot Analytics Engine
        response = requests.get("http://localhost:8080/api/reports/livestock/pdf")
        if response.status_code == 200:
            return HttpResponse(response.content, content_type="application/pdf")
        else:
            logger.log(f"Analytics engine returned status {response.status_code}")
            messages.error(request, f"Analytics Engine is currently unavailable.")
            return redirect("reports")
    except Exception as e:
        logger.log(f"Error calling analytics engine: {e}")
        messages.error(request, f"Analytics Engine Unavailable: {str(e)}")
        return redirect("reports")
