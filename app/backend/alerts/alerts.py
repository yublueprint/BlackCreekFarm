from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from app.backend.models import Alert
from app.logging.logging import Logger

logger = Logger("app/logging/app.log")


@login_required
def alerts_list(request):
    logger.log(f"User {request.user} viewed alerts history.")

    # Get all alerts, unread first, then by timestamp
    alerts = Alert.objects.all().order_by("is_read", "-timestamp")

    paginator = Paginator(alerts, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "app/alerts_list.html", context)


@login_required
def mark_alert_read(request, alert_id):
    try:
        alert = Alert.objects.get(id=alert_id)
        alert.is_read = True
        alert.save()
        logger.log(f"User {request.user} marked alert {alert_id} as read.")
    except Alert.DoesNotExist:
        pass

    return redirect("alerts_list")


@login_required
def mark_all_alerts_read(request):
    Alert.objects.filter(is_read=False).update(is_read=True)
    logger.log(f"User {request.user} marked all alerts as read.")
    return redirect("alerts_list")
