from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from app.exceptions.equipment.exception import (EquipmentCreationException,
                                                EquipmentDeleteException,
                                                EquipmentEditException)
from app.logging.logging import Logger

from ...forms.search_filtering_forms.EquipmentSearchForm import \
    EquipmentSearchForm
from ...functions.editStockNameChange import editStockNameChange
from ...functions.paginationFunction import paginationFunction
from ...models import (DEFAULT_FILLER_TEXT, DEFAULT_TEXT_MAX_LENGTH,
                       TEXTBOX_MAX_LENGTH, UNIT_INPUT_MAX_LENGTH, Equipment)

logger = Logger("app/logging/app.log")


def get_properties(request, ExceptionToUse: Exception):
    """
    Gets properties of equipment and validates the inputs.
    """
    # Mandatory fields.
    name = (request.POST.get("name") or "").strip() or DEFAULT_FILLER_TEXT
    category = (request.POST.get("category") or "").strip() or DEFAULT_FILLER_TEXT
    type = (request.POST.get("type") or "").strip() or DEFAULT_FILLER_TEXT
    # Optional fields.
    serial_number = (
        request.POST.get("serial_number") or ""
    ).strip() or DEFAULT_FILLER_TEXT
    purchase_date = request.POST.get("purchase_date") or None
    maintenance_due = request.POST.get("maintenance_due") or None
    next_checkup = request.POST.get("next_checkup") or None
    warranty_expiry = request.POST.get("warranty_expiry") or None
    location = (request.POST.get("location") or "").strip() or DEFAULT_FILLER_TEXT
    supplier = (request.POST.get("supplier") or "").strip() or DEFAULT_FILLER_TEXT
    hours_used = request.POST.get("hours_used") or None
    condition = (request.POST.get("condition") or "").strip() or DEFAULT_FILLER_TEXT
    purchase_cost = request.POST.get("purchase_cost") or 0
    active = request.POST.get("active") or "Yes"
    last_service_by = (
        request.POST.get("last_service_by") or ""
    ).strip() or DEFAULT_FILLER_TEXT
    service_interval_days = request.POST.get("service_interval_days") or 0
    maintenance_history = request.POST.get("maintenance_history") or ""
    notes = request.POST.get("notes") or ""

    required_inputs = {
        "name": name,
        "category": category,
        "type": type,
    }

    default_text_inputs_given = {
        "name": name,
        "category": category,
        "type": type,
        "serial_number": serial_number,
        "location": location,
        "supplier": supplier,
        "condition": condition,
        "last_service_by": last_service_by,
    }

    unit_inputs_given = {
        "hours_used": hours_used,
        "purchase_cost": purchase_cost,
        "service_interval_days": service_interval_days,
    }

    textbox_inputs_given = {
        "maintenance_history": maintenance_history,
        "notes": notes,
    }

    # Raise an error if mandatory fields are missing.
    for key, value in required_inputs.items():
        if value is None:
            raise ExceptionToUse(f"Missing {key} for supply.")

    inputs_given_list = [
        (default_text_inputs_given, DEFAULT_TEXT_MAX_LENGTH),
        (unit_inputs_given, UNIT_INPUT_MAX_LENGTH),
        (textbox_inputs_given, TEXTBOX_MAX_LENGTH),
    ]

    # check length if the optional field was actually provided.
    for input_given, max_length in inputs_given_list:
        for key, value in input_given.items():
            if (
                value
                and isinstance(value, str)
                and isinstance(value, str)
                and len(value) > max_length
            ):
                raise ExceptionToUse(
                    f"Equipment {key} input must be less than or equal to {max_length} characters."
                )

    return (
        name,
        category,
        type,
        serial_number,
        purchase_date,
        maintenance_due,
        next_checkup,
        warranty_expiry,
        location,
        supplier,
        hours_used,
        condition,
        purchase_cost,
        active,
        last_service_by,
        service_interval_days,
        maintenance_history,
        notes,
    )


def search_filtering(form):
    equipment = Equipment.objects.all().order_by("-id")
    active_filters = []

    if form.is_valid():
        data = form.cleaned_data

        if data.get("id"):
            equipment = equipment.filter(id=data["id"])
            active_filters.append(f"ID: {str(data['id'])}")
        if data.get("name"):
            equipment = equipment.filter(name__icontains=data["name"])
            active_filters.append(f"Name: {str(data['name'])}")
        if data.get("category"):
            equipment = equipment.filter(category__icontains=data["category"])
            active_filters.append(f"Category: {str(data['category'])}")
        if data.get("type"):
            equipment = equipment.filter(type__icontains=data["type"])
            active_filters.append(f"Type: {str(data['type'])}")
        if data.get("serial_number"):
            equipment = equipment.filter(serial_number__icontains=data["serial_number"])
            active_filters.append(f"Serial Number: {str(data['serial_number'])}")
        if data.get("purchase_date_mode"):
            if data.get("purchase_date_mode") != "all":
                if data.get("min_purchase_date") is not None:
                    equipment = equipment.filter(
                        purchase_date__gte=data["min_purchase_date"]
                    )
                    active_filters.append(
                        f"Min Purchase Date: {str(data['min_purchase_date'])}"
                    )
                if data.get("max_purchase_date") is not None:
                    equipment = equipment.filter(
                        purchase_date__lte=data["max_purchase_date"]
                    )
                    active_filters.append(
                        f"Max Purchase Date: {str(data['max_purchase_date'])}"
                    )
                if data.get("purchase_date_mode") == "highest":
                    equipment = equipment.order_by("-purchase_date")
                    active_filters.append("Highest to Lowest Purchase Date")
                if data.get("purchase_date_mode") == "lowest":
                    equipment = equipment.order_by("purchase_date")
                    active_filters.append("Lowest to Highest Purchase Date")
        if data.get("maintenance_date_mode"):
            if data.get("maintenance_date_mode") != "all":
                if data.get("min_maintenance_date") is not None:
                    equipment = equipment.filter(
                        maintenance_due__gte=data["min_maintenance_date"]
                    )
                    active_filters.append(
                        f"Min Maintenance Date: {str(data['min_maintenance_date'])}"
                    )
                if data.get("max_maintenance_date") is not None:
                    equipment = equipment.filter(
                        maintenance_due__lte=data["max_maintenance_date"]
                    )
                    active_filters.append(
                        f"Max Maintenance Date: {str(data['max_maintenance_date'])}"
                    )
                if data.get("maintenance_date_mode") == "highest":
                    equipment = equipment.order_by("-maintenance_due")
                    active_filters.append("Highest to Lowest Maintenance Date")
                if data.get("maintenance_date_mode") == "lowest":
                    equipment = equipment.order_by("maintenance_due")
                    active_filters.append("Lowest to Highest Maintenance Date")
        if data.get("next_checkup_mode"):
            if data.get("next_checkup_mode") != "all":
                if data.get("min_next_checkup") is not None:
                    equipment = equipment.filter(
                        next_checkup__gte=data["min_next_checkup"]
                    )
                    active_filters.append(
                        f"Min Next Checkup: {str(data['min_next_checkup'])}"
                    )
                if data.get("max_next_checkup") is not None:
                    equipment = equipment.filter(
                        next_checkup__lte=data["max_next_checkup"]
                    )
                    active_filters.append(
                        f"Max Next Checkup: {str(data['max_next_checkup'])}"
                    )
                if data.get("next_checkup_mode") == "highest":
                    equipment = equipment.order_by("-next_checkup")
                    active_filters.append("Highest to Lowest Next Checkup")
                if data.get("next_checkup_mode") == "lowest":
                    equipment = equipment.order_by("next_checkup")
                    active_filters.append("Lowest to Highest Next Checkup")
        if data.get("warranty_expiration_mode"):
            if data.get("warranty_expiration_mode") != "all":
                if data.get("min_warranty_expiration") is not None:
                    equipment = equipment.filter(
                        warranty_expiry__gte=data["min_warranty_expiration"]
                    )
                    active_filters.append(
                        f"Min Warranty Expiration: {str(data['min_warranty_expiration'])}"
                    )
                if data.get("max_next_checkup") is not None:
                    equipment = equipment.filter(
                        warranty_expiry__lte=data["max_warranty_expiration"]
                    )
                    active_filters.append(
                        f"Max Warranty Expiration: {str(data['max_warranty_expiration'])}"
                    )
                if data.get("warranty_expiration_mode") == "highest":
                    equipment = equipment.order_by("-warranty_expiry")
                    active_filters.append("Highest to Lowest Warranty Expiration")
                if data.get("warranty_expiration_mode") == "lowest":
                    equipment = equipment.order_by("warranty_expiry")
                    active_filters.append("Lowest to Highest Warranty Expiration")
        if data.get("location"):
            equipment = equipment.filter(location__icontains=data["location"])
            active_filters.append(f"Location: {str(data['location'])}")
        if data.get("supplier"):
            equipment = equipment.filter(supplier__icontains=data["supplier"])
            active_filters.append(f"Supplier: {str(data['supplier'])}")
        if data.get("hours_used_mode"):
            if data.get("hours_used_mode") != "all":
                if data.get("min_hours_used") is not None:
                    equipment = equipment.filter(hours_used__gte=data["min_hours_used"])
                    active_filters.append(
                        f"Min Hours Used: {str(data['min_hours_used'])}"
                    )
                if data.get("max_hours_used") is not None:
                    equipment = equipment.filter(hours_used__lte=data["max_hours_used"])
                    active_filters.append(
                        f"Max Hours Used: {str(data['max_hours_used'])}"
                    )
                if data.get("hours_used_mode") == "highest":
                    equipment = equipment.order_by("-hours_used")
                    active_filters.append("Highest to Lowest Hours Used")
                if data.get("hours_used_mode") == "lowest":
                    equipment = equipment.order_by("hours_used")
                    active_filters.append("Lowest to Highest Hours Used")
        if data.get("condition"):
            equipment = equipment.filter(condition__icontains=data["condition"])
            active_filters.append(f"Condition: {str(data['condition'])}")
        if data.get("purchase_cost_mode"):
            if data.get("purchase_cost_mode") != "all":
                if data.get("min_purchase_cost") is not None:
                    equipment = equipment.filter(
                        purchase_cost__gte=data["min_purchase_cost"]
                    )
                    active_filters.append(
                        f"Min Purchase Cost: {str(data['min_purchase_cost'])}"
                    )
                if data.get("max_purchase_cost") is not None:
                    equipment = equipment.filter(
                        purchase_cost__lte=data["max_purchase_cost"]
                    )
                    active_filters.append(
                        f"Max Purchase Cost: {str(data['max_purchase_cost'])}"
                    )
                if data.get("purchase_cost_mode") == "highest":
                    equipment = equipment.order_by("-purchase_cost")
                    active_filters.append("Highest to Lowest Purchase Cost")
                if data.get("purchase_cost_mode") == "lowest":
                    equipment = equipment.order_by("purchase_cost")
                    active_filters.append("Lowest to Highest Purchase Cost")
        if data.get("active"):
            if data.get("active") != "None":
                equipment = equipment.filter(active__icontains=data["active"])
                active_filters.append(f"Active: {str(data['active'])}")
        if data.get("last_service_by"):
            equipment = equipment.filter(
                last_service_by__icontains=data["last_service_by"]
            )
            active_filters.append(f"Condition: {str(data['last_service_by'])}")
        if data.get("service_interval_days_mode"):
            if data.get("service_interval_days_mode") != "all":
                if data.get("min_service_interval_days") is not None:
                    equipment = equipment.filter(
                        service_interval_days__gte=data["min_service_interval_days"]
                    )
                    active_filters.append(
                        f"Min Service Interval Days: {str(data['min_service_interval_days'])}"
                    )
                if data.get("max_service_interval_days") is not None:
                    equipment = equipment.filter(
                        service_interval_days__lte=data["max_service_interval_days"]
                    )
                    active_filters.append(
                        f"Max Service Interval Days: {str(data['max_service_interval_days'])}"
                    )
                if data.get("service_interval_days_mode") == "highest":
                    equipment = equipment.order_by("-service_interval_days")
                    active_filters.append("Highest to Lowest Service Interval Days")
                if data.get("service_interval_days_mode") == "lowest":
                    equipment = equipment.order_by("service_interval_days")
                    active_filters.append("Lowest to Highest Service Interval Days")
    return active_filters, equipment


@login_required
def equipment_list(request, id=None):
    try:
        # FOR SEARCH FILTERING.
        form = EquipmentSearchForm(request.GET)
        active_filters, equipment = search_filtering(form)

        # If ID was given in URL. Ex: equipment/id/<int>
        if id:
            base_url = reverse("equipment_list")
            query_string = urlencode({"id": id})
            return redirect(f"{base_url}?{query_string}")

        # FOR PAGINATION.
        page_number = request.GET.get("page")
        page_obj, backward_pages, forward_pages, page_number = paginationFunction(
            equipment, page_number, 10
        )

        context = {
            "form": form,
            "search_filters_applied": active_filters,
            "list_url_given": "equipment_list",
            "add_url_given": "add_equipment",
            "edit_url_given": "edit_equipment",
            "delete_url_given": "delete_equipment",
            "page_obj": page_obj,
            "backward_pages": backward_pages,
            "forward_pages": forward_pages,
            "max_textbox_length": TEXTBOX_MAX_LENGTH,
            "max_input_text_length": DEFAULT_TEXT_MAX_LENGTH,
            "max_input_unit_length": UNIT_INPUT_MAX_LENGTH,
        }

        logger.log(f"User {request.user} viewed equipment list (page {page_number}).")
        return render(request, "app/equipment_list.html", context)
    except Exception as e:
        logger.log(f"Error in equipment view by {request.user}: {e}")
        messages.error(request, str(e))
        return redirect("error_page")


@login_required
def add_equipment(request):
    if request.method == "POST":
        try:
            (
                name,
                category,
                type,
                serial_number,
                purchase_date,
                maintenance_due,
                next_checkup,
                warranty_expiry,
                location,
                supplier,
                hours_used,
                condition,
                purchase_cost,
                active,
                last_service_by,
                service_interval_days,
                maintenance_history,
                notes,
            ) = get_properties(request, EquipmentCreationException)

            equipment = Equipment.objects.create(
                name=name,
                category=category,
                type=type,
                purchase_date=purchase_date,
                maintenance_due=maintenance_due,
                hours_used=hours_used,
                condition=condition,
                next_checkup=next_checkup,
                purchase_cost=purchase_cost,
                notes=notes,
                serial_number=serial_number,
                location=location,
                warranty_expiry=warranty_expiry,
                supplier=supplier,
                maintenance_history=maintenance_history,
                active=active,
                last_service_by=last_service_by,
                service_interval_days=service_interval_days,
            )

            logger.log(
                f"User {request.user} added equipment: {equipment.name} (ID: {equipment.id})."
            )
            return redirect("equipment_list")

        except EquipmentCreationException as e:
            logger.log(f"Equipment creation error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("equipment_list")
        except Exception as e:
            logger.log(
                f"Unexpected error during equipment creation by user {request.user}: {e}"
            )
            messages.error(
                request, "An unexpected error occurred while adding the equipment."
            )
            return redirect("equipment_list")
    return redirect("equipment_list")


@login_required
def edit_equipment(request):
    if request.method == "POST":
        try:
            try:
                equipment = get_object_or_404(Equipment, id=request.POST.get("id"))
            except Http404:
                raise EquipmentEditException("Equipment not found.")

            old_name = equipment.name

            (
                equipment.name,
                equipment.category,
                equipment.type,
                equipment.serial_number,
                equipment.purchase_date,
                equipment.maintenance_due,
                equipment.next_checkup,
                equipment.warranty_expiry,
                equipment.location,
                equipment.supplier,
                equipment.hours_used,
                equipment.condition,
                equipment.purchase_cost,
                equipment.active,
                equipment.last_service_by,
                equipment.service_interval_days,
                equipment.maintenance_history,
                equipment.notes,
            ) = get_properties(request, EquipmentEditException)

            equipment.save()

            name_change_msg = editStockNameChange(old_name, equipment.name)

            logger.log(
                f"User {request.user} edited equipment: {old_name}{name_change_msg} (ID: {equipment.id})."
            )
            return redirect("equipment_list")

        except EquipmentEditException as e:
            logger.log(f"Equipment edit error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("equipment_list")
        except Exception as e:
            logger.log(
                f"Unexpected error during equipment edit by user {request.user}: {e}"
            )
            messages.error(
                request, "An unexpected error occurred while editing the equipment."
            )
            return redirect("equipment_list")
    return redirect("equipment_list")


@login_required
def delete_equipment(request):
    if request.method == "POST":
        try:
            try:
                equipment = get_object_or_404(Equipment, id=request.POST.get("id"))
            except Http404:
                raise EquipmentDeleteException("Equipment not found.")

            equipment_name = equipment.name or "Unknown"
            equipment_id = equipment.id or -1
            equipment.delete()

            logger.log(
                f"User {request.user} deleted equipment: {equipment_name} (ID: {equipment_id})."
            )
            return redirect("equipment_list")

        except EquipmentDeleteException as e:
            logger.log(f"Equipment delete error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("equipment_list")
        except Exception as e:
            logger.log(
                f"Unexpected error during equipment deletion by user {request.user}: {e}"
            )
            messages.error(
                request, "An unexpected error occurred while deleting the equipment."
            )
            return redirect("equipment_list")
    return redirect("equipment_list")
