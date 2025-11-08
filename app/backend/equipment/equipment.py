from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from app.exceptions.equipment.exception import (EquipmentCreationException,
                                                EquipmentDeleteException,
                                                EquipmentEditException)
from app.logging.logging import Logger

from ..models import Equipment

logger = Logger("app/logging/app.log")


@login_required
def equipment_list(request):
    equipment = Equipment.objects.all()
    logger.log(f"User {request.user} viewed equipment list.")
    return render(request, "app/equipment_list.html", {"equipment": equipment})


@login_required
def add_equipment(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            equipment_type = request.POST.get("type")  # avoid shadowing builtin `type`
            purchase_date = request.POST.get("purchase_date")
            maintenance_due = request.POST.get("maintenance_due")

            if (
                not name
                or not equipment_type
                or not purchase_date
                or not maintenance_due
            ):
                raise EquipmentCreationException("All fields are required.")

            Equipment.objects.create(
                name=name,
                type=equipment_type,
                purchase_date=purchase_date,
                maintenance_due=maintenance_due,
            )

            logger.log(f"User {request.user} added equipment: {name}")
            return redirect("equipment_list")

        except EquipmentCreationException as e:
            logger.log(f"Equipment creation error by {request.user}: {e}")
            equipment = Equipment.objects.all()
            return render(
                request,
                "app/equipment_list.html",
                {"equipment": equipment, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during equipment creation: {e}")
            equipment = Equipment.objects.all()
            return render(
                request,
                "app/equipment_list.html",
                {
                    "equipment": equipment,
                    "error": "An unexpected error occurred while adding the equipment.",
                },
            )
    return redirect("equipment_list")


@login_required
def edit_equipment(request):
    if request.method == "POST":
        try:
            try:
                equipment = get_object_or_404(Equipment, id=request.POST.get("id"))
            except Http404:
                raise EquipmentEditException("Equipment not found.")

            equipment.name = request.POST.get("name")
            equipment.type = request.POST.get("type")
            equipment.purchase_date = request.POST.get("purchase_date")
            equipment.maintenance_due = request.POST.get("maintenance_due")

            if (
                not equipment.name
                or not equipment.type
                or not equipment.purchase_date
                or not equipment.maintenance_due
            ):
                raise EquipmentEditException(
                    "All fields are required to update equipment."
                )

            equipment.save()

            logger.log(f"User {request.user} edited equipment: {equipment.name}")
            return redirect("equipment_list")

        except EquipmentEditException as e:
            logger.log(f"Equipment edit error by {request.user}: {e}")
            equipment = Equipment.objects.all()
            return render(
                request,
                "app/equipment_list.html",
                {"equipment": equipment, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during equipment edit: {e}")
            equipment = Equipment.objects.all()
            return render(
                request,
                "app/equipment_list.html",
                {
                    "equipment": equipment,
                    "error": "An unexpected error occurred while editing the equipment.",
                },
            )
    return redirect("equipment_list")


@login_required
def delete_equipment(request):
    if request.method == "POST":
        try:
            try:
                equipment = get_object_or_404(Equipment, id=request.POST.get("id"))
            except Http404:
                raise EquipmentDeleteException("Equipment not found.")

            equipment_name = equipment.name
            equipment.delete()

            logger.log(f"User {request.user} deleted equipment: {equipment_name}")
            return redirect("equipment_list")

        except EquipmentDeleteException as e:
            logger.log(f"Equipment delete error by {request.user}: {e}")
            equipment = Equipment.objects.all()
            return render(
                request,
                "app/equipment_list.html",
                {"equipment": equipment, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during equipment deletion: {e}")
            equipment = Equipment.objects.all()
            return render(
                request,
                "app/equipment_list.html",
                {
                    "equipment": equipment,
                    "error": "An unexpected error occurred while deleting the equipment.",
                },
            )
    return redirect("equipment_list")
