from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
<<<<<<< HEAD
            name = (request.POST.get("name") or "").strip()
            category = (request.POST.get("category") or "").strip()
            equipment_type = (request.POST.get("type") or "").strip()  # avoid shadowing builtin `type`

            # Optional fields: convert "" -> None
            purchase_date = (request.POST.get("purchase_date") or "").strip() or None
            maintenance_due = (request.POST.get("maintenance_due") or "").strip() or None
            notes = (request.POST.get("notes") or "").strip() or None

            if not name or not category or not equipment_type:
                raise EquipmentCreationException("Name, Category, and Type are required.")
=======
            name = request.POST.get("name")
            category = request.POST.get("category")
            equipment_type = request.POST.get("type")
            serial_number = request.POST.get("serial_number")
            purchase_date = request.POST.get("purchase_date")
            maintenance_due = request.POST.get("maintenance_due")
            next_checkup = request.POST.get("next_checkup")
            warranty_expiry = request.POST.get("warranty_expiry")
            location = request.POST.get("location")
            supplier = request.POST.get("supplier")
            hours_used = request.POST.get("hours_used")
            condition = request.POST.get("condition")
            purchase_cost = request.POST.get("purchase_cost")
            active = request.POST.get("active") == "on"
            last_service_by = request.POST.get("last_service_by")
            service_interval_days = request.POST.get("service_interval_days")
            maintenance_history = request.POST.get("maintenance_history")
            notes = request.POST.get("notes")
            required_fields = [
                name,
                category,
                equipment_type,
                purchase_date,
                maintenance_due,
            ]
            if not all(required_fields):
                raise EquipmentCreationException(
                    "Name, category, type, purchase and maintenance dates are required."
                )
>>>>>>> origin/prod

            Equipment.objects.create(
                name=name,
                category=category,
                type=equipment_type,
                purchase_date=purchase_date,
                maintenance_due=maintenance_due,
<<<<<<< HEAD
                notes=notes,
=======
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
>>>>>>> origin/prod
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

<<<<<<< HEAD
            name = (request.POST.get("name") or "").strip()
            category = (request.POST.get("category") or "").strip()
            equipment_type = (request.POST.get("type") or "").strip()

            # Optional fields: convert "" -> None
            purchase_date = (request.POST.get("purchase_date") or "").strip() or None
            maintenance_due = (request.POST.get("maintenance_due") or "").strip() or None
            notes = (request.POST.get("notes") or "").strip() or None

            if not name or not category or not equipment_type:
                raise EquipmentEditException("Name, Category, and Type are required.")

            equipment.name = name
            equipment.category = category
            equipment.type = equipment_type
            equipment.purchase_date = purchase_date
            equipment.maintenance_due = maintenance_due
            equipment.notes = notes

=======
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
            equipment.service_interval_days = int(
                request.POST.get("service_interval_days") or 0
            )

            if (
                not equipment.name
                or not equipment.category
                or not equipment.type
                or not equipment.purchase_date
                or not equipment.maintenance_due
            ):
                raise EquipmentEditException(
                    "Name, category, type, purchase and maintenance dates are required to "
                    "update equipment."
                )
>>>>>>> origin/prod
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
