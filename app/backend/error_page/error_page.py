from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.logging.logging import Logger

logger = Logger("app/logging/app.log")


@login_required
def error_page(request):
    context = {}

    logger.log(f"User {request.user} viewed error page.")
    return render(request, "app/error_page.html", context)
