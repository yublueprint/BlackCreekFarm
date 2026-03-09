from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from app.exceptions.equipment.exception import (
    EquipmentCreationException,
    EquipmentDeleteException,
    EquipmentEditException,
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
            name = (request.POST.get("name") or "").strip()
            category = (request.POST.get("category") or "").strip()
            equipment_type = (
                request.POST.get("type") or ""
            ).strip()  # avoid shadowing builtin type

            # Optional fields: convert "" -> None
            purchase_date = (request.POST.get("purchase_date") or "").strip() or None
            maintenance_due = (
                request.POST.get("maintenance_due") or ""
            ).strip() or None
            notes = (request.POST.get("notes") or "").strip() or None

            # ONLY required fields
            if not name or not category or not equipment_type:
                raise EquipmentCreationException(
                    "Name, Category, and Type are required."
                )

            Equipment.objects.create(
                name=name,
                category=category,
                type=equipment_type,
                purchase_date=purchase_date,
                maintenance_due=maintenance_due,
                notes=notes,
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

            name = (request.POST.get("name") or "").strip()
            category = (request.POST.get("category") or "").strip()
            equipment_type = (request.POST.get("type") or "").strip()

            purchase_date = (request.POST.get("purchase_date") or "").strip() or None
            maintenance_due = (
                request.POST.get("maintenance_due") or ""
            ).strip() or None
            notes = (request.POST.get("notes") or "").strip() or None

            # ONLY required fields
            if not name or not category or not equipment_type:
                raise EquipmentEditException("Name, Category, and Type are required.")

            equipment.name = name
            equipment.category = category
            equipment.type = equipment_type
            equipment.purchase_date = purchase_date
            equipment.maintenance_due = maintenance_due
            equipment.notes = notes

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
            logger.log(f"Unexpected error during equipment deletion: {e}")
            equipment_qs = Equipment.objects.all().order_by("id")
            paginator = Paginator(equipment_qs, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(
                request,
                "app/equipment_list.html",
                {
                    "equipment": page_obj,
                    "error": "An unexpected error occurred while deleting the equipment.",
                },
            )
    return redirect("equipment_list")
