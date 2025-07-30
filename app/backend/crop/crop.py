from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from app.logging.logging import Logger

from ..models import Crop

logger = Logger("app/logging/app.log")


@login_required
def crop_list(request):
    crops = Crop.objects.all()
    logger.log(f"User {request.user} viewed crop list.")
    return render(request, "app/crop_list.html", {"crops": crops})


@login_required
def add_crop(request):
    if request.method == "POST":
        name = request.POST.get("name")
        planting_date = request.POST.get("planting_date")
        harvest_date = request.POST.get("harvest_date")
        yield_estimate = request.POST.get("yield_estimate")
        purchase_date = request.POST.get("purchase_date")
        quantity = request.POST.get("quantity")
        notes = request.POST.get("notes")

        Crop.objects.create(
            name=name,
            planting_date=planting_date,
            harvest_date=harvest_date,
            yield_estimate=yield_estimate,
            purchase_date=purchase_date,
            quantity=quantity,
            notes=notes,
        )
        logger.log(f"User {request.user} added crop: {name}")
        return redirect("crop_list")
    


@login_required
def edit_crop(request):
    if request.method == "POST":
        crop = get_object_or_404(Crop, id=request.POST.get("id"))
        old_name = crop.name
        crop.name = request.POST.get("name")
        crop.purchase_date = request.POST.get("purchase_date")
        crop.planting_date = request.POST.get("planting_date")
        crop.harvest_date = request.POST.get("harvest_date")
        crop.quantity = request.POST.get("quantity")
        crop.yield_estimate = request.POST.get("yield_estimate")
        crop.notes = request.POST.get("notes")
        crop.save()
        logger.log(f"User {request.user} edited crop: {old_name} to {crop.name}")
        return redirect("crop_list")


@login_required
def delete_crop(request):
    if request.method == "POST":
        crop = get_object_or_404(Crop, id=request.POST.get("id"))
        crop_name = crop.name
        crop.delete()
        logger.log(f"User {request.user} deleted crop: {crop_name}")
        return redirect("crop_list")
