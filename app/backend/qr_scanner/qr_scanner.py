from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.logging.logging import Logger

from ..models import (Crop, Equipment, Livestock, Supplies, Transaction)

logger = Logger("app/logging/app.log")

@login_required
def qr_scanner_page(request):
    try:
        context = {}

        logger.log(f"User {request.user} viewed QR Scanner page.")
        return render(request, "app/qr_scanner/qr_scanner_page.html", context)
    except Exception as e:
        logger.log(f"Error in QR Scanner view by {request.user}: {e}")
        messages.error(request, str(e))
        return redirect("error_page")
    
@login_required
def qr_scanner_camera(request):
    try:
        context = {}

        logger.log(f"User {request.user} viewed QR Scanner Camera page.")
        return render(request, "app/qr_scanner/qr_scanner_camera.html", context)
    except Exception as e:
        logger.log(f"Error in QR Scanner Camera view by {request.user}: {e}")
        messages.error(request, str(e))
        return redirect("qr_scanner_page")
    
@login_required
def manually_find_item(request):
    try:
        stock_chosen = request.POST.get("stock_selector")
        id_chosen = request.POST.get("stock_id")

        if not stock_chosen:
            raise Exception(f"Please select a stock.")
        if not id_chosen:
            raise Exception(f"Please enter an ID.")

        valid_options = ["Livestock", "Crop", "Equipment", "Supplies", "Transactions"]

        if stock_chosen in valid_options:
            if stock_chosen == "Livestock":
                return redirect(f"/livestock/?id={id_chosen}")
            elif stock_chosen == "Crop":
                return redirect(f"/crops/?id={id_chosen}")
            elif stock_chosen == "Equipment":
                return redirect(f"/equipment/?id={id_chosen}")
            elif stock_chosen == "Supplies":
                return redirect(f"/supplies/?id={id_chosen}")
            elif stock_chosen == "Transactions":
                return redirect(f"/transactions/?id={id_chosen}")
        else:
            raise Exception(f"{stock_chosen} is not a valid option.")
    except Exception as e:
        logger.log(
            f"Error while manually finding item of {stock_chosen} by {request.user}: {e}"
        )
        messages.error(request, str(e))
        return redirect("qr_scanner_page")