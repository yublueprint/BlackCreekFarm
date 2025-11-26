from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.core.paginator import Paginator

from app.exceptions.equipment.exception import (
    EquipmentCreationException,
    EquipmentEditException,
    EquipmentDeleteException,
)
from app.logging.logging import Logger
from ..models import Equipment

logger = Logger("app/logging/app.log")


@login_required
def equipment_list(request):
    equipment_qs = Equipment.objects.all().order_by("id")
    paginator = Paginator(equipment_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    logger.log(f"User {request.user} viewed equipment list.")
    return render(request, "app/equipment_list.html", {"equipment": page_obj})


@login_required
def add_equipment(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            category = request.POST.get("category")
            equipment_type = request.POST.get("type")
            purchase_date = request.POST.get("purchase_date")
            maintenance_due = request.POST.get("maintenance_due")
            hours_used = request.POST.get("hours_used")
            condition = request.POST.get("condition")
            next_checkup = request.POST.get("next_checkup")
            purchase_cost = request.POST.get("purchase_cost")
            notes = request.POST.get("notes")
            serial_number = request.POST.get("serial_number")
            location = request.POST.get("location")
            warranty_expiry = request.POST.get("warranty_expiry")
            supplier = request.POST.get("supplier")
            maintenance_history = request.POST.get("maintenance_history")
            active = request.POST.get("active") == "on"
            last_service_by = request.POST.get("last_service_by")
            service_interval_days = request.POST.get("service_interval_days")

            if not name or not category or not equipment_type or not purchase_date or not maintenance_due:
                raise EquipmentCreationException("Name, category, type, purchase and maintenance dates are required.")

            Equipment.objects.create(
                name=name,
                category=category,
                type=equipment_type,
                purchase_date=purchase_date,
                maintenance_due=maintenance_due,
                hours_used=float(hours_used or 0),
                condition=condition or "Good",
                next_checkup=next_checkup or None,
                purchase_cost=float(purchase_cost or 0),
                notes=notes,
                serial_number=serial_number,
                location=location,
                warranty_expiry=warranty_expiry or None,
                supplier=supplier,
                maintenance_history=maintenance_history,
                active=active,
                last_service_by=last_service_by,
                service_interval_days=int(service_interval_days or 0),
            )

            logger.log(f"User {request.user} added equipment: {name}")
            return redirect("equipment_list")

        except EquipmentCreationException as e:
            logger.log(f"Equipment creation error by {request.user}: {e}")
            equipment_qs = Equipment.objects.all().order_by("id")
            paginator = Paginator(equipment_qs, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(
                request,
                "app/equipment_list.html",
                {"equipment": page_obj, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during equipment creation: {e}")
            equipment_qs = Equipment.objects.all().order_by("id")
            paginator = Paginator(equipment_qs, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(
                request,
                "app/equipment_list.html",
                {
                    "equipment": page_obj,
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
            equipment.category = request.POST.get("category")
            equipment.type = request.POST.get("type")
            equipment.purchase_date = request.POST.get("purchase_date")
            equipment.maintenance_due = request.POST.get("maintenance_due")
            equipment.hours_used = float(request.POST.get("hours_used") or 0)
            equipment.condition = request.POST.get("condition") or "Good"
            equipment.next_checkup = request.POST.get("next_checkup") or None
            equipment.purchase_cost = float(request.POST.get("purchase_cost") or 0)
            equipment.notes = request.POST.get("notes")
            equipment.serial_number = request.POST.get("serial_number")
            equipment.location = request.POST.get("location")
            equipment.warranty_expiry = request.POST.get("warranty_expiry") or None
            equipment.supplier = request.POST.get("supplier")
            equipment.maintenance_history = request.POST.get("maintenance_history")
            equipment.active = request.POST.get("active") == "on"
            equipment.last_service_by = request.POST.get("last_service_by")
            equipment.service_interval_days = int(request.POST.get("service_interval_days") or 0)

            if (
                not equipment.name
                or not equipment.category
                or not equipment.type
                or not equipment.purchase_date
                or not equipment.maintenance_due
            ):
                raise EquipmentEditException("Name, category, type, purchase and maintenance dates are required to update equipment.")

            equipment.save()

            logger.log(f"User {request.user} edited equipment: {equipment.name}")
            return redirect("equipment_list")

        except EquipmentEditException as e:
            logger.log(f"Equipment edit error by {request.user}: {e}")
            equipment_qs = Equipment.objects.all().order_by("id")
            paginator = Paginator(equipment_qs, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(
                request,
                "app/equipment_list.html",
                {"equipment": page_obj, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during equipment edit: {e}")
            equipment_qs = Equipment.objects.all().order_by("id")
            paginator = Paginator(equipment_qs, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(
                request,
                "app/equipment_list.html",
                {
                    "equipment": page_obj,
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
