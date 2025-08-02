from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from app.logging.logging import Logger

from ..models import Equipment

logger = Logger("app/logging/app.log")


@login_required
def equipment_list(request):
    equipment = Equipment.objects.all()
    today = timezone.now().date()
    logger.log(f"User {request.user} viewed equipment list.")
    return render(request, "app/equipment_list.html", {"equipment": equipment, "today": today})


@login_required
def add_equipment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        purchase_date = request.POST.get("purchase_date")
        maintenance_due = request.POST.get("maintenance_due")
        quantity = request.POST.get("quantity")
        notes = request.POST.get("notes")

        Equipment.objects.create(
            name=name,
            category=category,
            purchase_date=purchase_date,
            maintenance_due=maintenance_due,
            quantity=quantity,
            notes=notes,
        )
        logger.log(f"User {request.user} added equipment: {name}")
        return redirect("equipment_list")


@login_required
def edit_equipment(request):
    if request.method == "POST":
        equipment = get_object_or_404(Equipment, id=request.POST.get("id"))
        old_name = equipment.name
        equipment.name = request.POST.get("name")
        equipment.category = request.POST.get("category")
        equipment.purchase_date = request.POST.get("purchase_date")
        equipment.maintenance_due = request.POST.get("maintenance_due")
        equipment.quantity = request.POST.get("quantity")
        equipment.notes = request.POST.get("notes")
        equipment.save()
        logger.log(
            f"User {request.user} edited equipment: {old_name} to {equipment.name}"
        )
        return redirect("equipment_list")


@login_required
def delete_equipment(request):
    if request.method == "POST":
        equipment = get_object_or_404(Equipment, id=request.POST.get("id"))
        equipment_name = equipment.name
        equipment.delete()
        logger.log(f"User {request.user} deleted equipment: {equipment_name}")
        return redirect("equipment_list")