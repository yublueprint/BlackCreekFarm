from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from app.exceptions.supplies.exception import (SupplyCreationException,
                                               SupplyDeleteException,
                                               SupplyEditException)
from app.logging.logging import Logger

from ..forms import SuppliesSearchForm
from ..functions import paginationFunction, editStockNameChange
from ..models import (DEFAULT_TEXT_MAX_LENGTH, TEXTBOX_MAX_LENGTH,
                      UNIT_INPUT_MAX_LENGTH, Supplies)

logger = Logger("app/logging/app.log")


def get_properties(request, ExceptionToUse: Exception):
    """
    Gets properties of supplies and validates the inputs.
    """
    # Mandatory fields.
    name = (request.POST.get("name") or "").strip() or "Unknown"
    supply_category = (request.POST.get("supply_category") or "").strip() or "Unknown"
    quantity = request.POST.get("quantity") or -1
    # Optional fields.
    unit = (request.POST.get("unit") or "").strip() or "Unknown"
    last_restocked = request.POST.get("last_restocked") or None
    minimum_required = request.POST.get("minimum_required") or None
    cost_per_unit = request.POST.get("cost_per_unit") or None
    procurement_date = request.POST.get("procurement_date") or None
    notes = request.POST.get("notes") or ""

    required_inputs = {
        "name": name,
        "supply_category": supply_category,
        "quantity": quantity,
    }

    default_text_inputs_given = {
        "name": name,
        "supply_category": supply_category,
    }

    unit_inputs_given = {
        "unit": unit,
    }

    textbox_inputs_given = {
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
            if value and len(value) > max_length:
                raise ExceptionToUse(
                    f"Supply {key} input must be less or equal to {max_length} characters."
                )

    return (
        name,
        supply_category,
        quantity,
        unit,
        last_restocked,
        minimum_required,
        cost_per_unit,
        procurement_date,
        notes,
    )

def search_filtering(form):
    supplies = Supplies.objects.all().order_by("-id")
    active_filters = []

    if form.is_valid():
        data = form.cleaned_data

        if data.get("id"):
            supplies = supplies.filter(id=data["id"])
            active_filters.append(f"ID: {str(data['id'])}")
        if data.get("name"):
            supplies = supplies.filter(name__icontains=data["name"])
            active_filters.append(f"Name: {str(data['name'])}")
        if data.get("category"):
            supplies = supplies.filter(category__icontains=data["category"])
            active_filters.append(f"Category: {str(data['category'])}")
        if data.get("qty_mode"):
            if data.get("qty_mode") == "range":
                if data.get("min_qty") is not None:
                    supplies = supplies.filter(quantity__gte=data["min_qty"])
                    active_filters.append(f"Min Qty: {str(data['min_qty'])}")
                if data.get("max_qty") is not None:
                    supplies = supplies.filter(quantity__lte=data["max_qty"])
                    active_filters.append(f"Max Qty: {str(data['max_qty'])}")
        if data.get("unit"):
            supplies = supplies.filter(unit__icontains=data["unit"])
            active_filters.append(f"Unit: {str(data['unit'])}")
        if data.get("minimum_required"):
            supplies = supplies.filter(minimum_required__gte=data["minimum_required"])
            active_filters.append(f"Minimum Required: {str(data['minimum_required'])}")
        if data.get("cost_per_unit"):
            supplies = supplies.filter(cost_per_unit=data["cost_per_unit"])
            active_filters.append(f"Cost Per Unit: {str(data['cost_per_unit'])}")
        if data.get("last_restocked_mode"):
            if data.get("last_restocked_mode") == "range":
                if data.get("min_last_restocked") is not None:
                    supplies = supplies.filter(
                        last_restocked__gte=data["min_last_restocked"]
                    )
                    active_filters.append(
                        f"Min Last Restocked: {str(data['min_last_restocked'])}"
                    )
                if data.get("max_last_restocked") is not None:
                    supplies = supplies.filter(
                        last_restocked__lte=data["max_last_restocked"]
                    )
                    active_filters.append(
                        f"Max Last Restocked: {str(data['max_last_restocked'])}"
                    )
        if data.get("procurement_date_mode"):
            if data.get("procurement_date_mode") == "range":
                if data.get("min_procurement_date") is not None:
                    supplies = supplies.filter(
                        procurement_date__gte=data["min_procurement_date"]
                    )
                    active_filters.append(
                        f"Min Procurement Date: {str(data['min_procurement_date'])}"
                    )
                if data.get("max_procurement_date") is not None:
                    supplies = supplies.filter(
                        procurement_date__lte=data["max_procurement_date"]
                    )
                    active_filters.append(
                        f"Max Procurement Date: {str(data['max_procurement_date'])}"
                    )
    return active_filters, supplies

@login_required
def supplies_list(request):
    # FOR SEARCH FILTERING.
    form = SuppliesSearchForm(request.GET)
    active_filters, supplies = search_filtering(form)

    # FOR PAGINATION.
    page_number = request.GET.get("page")
    page_obj, backward_pages, forward_pages, page_number = paginationFunction(
        supplies, page_number, 10
    )

    context = {
        "form": form,
        "search_filters_applied": active_filters,
        "list_url_given": "supplies_list",
        "add_url_given": "add_supplies",
        "edit_url_given": "edit_supplies",
        "delete_url_given": "delete_supplies",
        "page_obj": page_obj,
        "backward_pages": backward_pages,
        "forward_pages": forward_pages,
        "max_textbox_length": TEXTBOX_MAX_LENGTH,
        "max_input_text_length": DEFAULT_TEXT_MAX_LENGTH,
        "max_input_unit_length": UNIT_INPUT_MAX_LENGTH,
    }

    logger.log(f"User {request.user} viewed supplies list (page {page_number}).")
    return render(request, "app/supplies_list.html", context)


@login_required
def add_supplies(request):
    if request.method == "POST":
        try:
            (
                name,
                supply_category,
                quantity,
                unit,
                last_restocked,
                minimum_required,
                cost_per_unit,
                procurement_date,
                notes,
            ) = get_properties(request, SupplyCreationException)

            supply = Supplies.objects.create(
                name=name,
                category=supply_category,
                quantity=quantity,
                unit=unit,
                last_restocked=last_restocked,
                minimum_required=minimum_required,
                cost_per_unit=cost_per_unit,
                procurement_date=procurement_date,
                notes=notes,
            )

            logger.log(f"User {request.user} added supply: {name} (ID: {supply.id}).")
            return redirect("supplies_list")

        except SupplyCreationException as e:
            logger.log(f"Supply creation error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("supplies_list")
        except Exception as e:
            logger.log(f"Unexpected error during supply creation: {e}")
            messages.error(request, "An unexpected error occurred while adding the supply.")
            return redirect("supplies_list")
    return redirect("supplies_list")


@login_required
def edit_supplies(request):
    if request.method == "POST":
        try:
            try:
                supply = get_object_or_404(Supplies, id=request.POST.get("id"))
            except Http404:
                raise SupplyEditException("Supply not found.")
            
            old_name = supply.name

            (
                supply.name,
                supply.category,
                supply.quantity,
                supply.unit,
                supply.last_restocked,
                supply.minimum_required,
                supply.cost_per_unit,
                supply.procurement_date,
                supply.notes,
            ) = get_properties(request, SupplyEditException)

            supply.save()

            name_change_msg = editStockNameChange(old_name, supply.name)

            logger.log(f"User {request.user} edited supply: {old_name} {name_change_msg} (ID: {supply.id}).")
            return redirect("supplies_list")

        except SupplyEditException as e:
            logger.log(f"Supply edit error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("supplies_list")
        except Exception as e:
            logger.log(f"Unexpected error during supply edit: {e}")
            messages.error(request, "An unexpected error occurred while editing the supply.")
            return redirect("supplies_list")
    return redirect("supplies_list")


@login_required
def delete_supplies(request):
    if request.method == "POST":
        try:
            try:
                supply = get_object_or_404(Supplies, id=request.POST.get("id"))
            except Http404:
                raise SupplyDeleteException("Supply not found.")

            supply_name = supply.name or "Unknown"
            supply_id = supply.id or -1
            supply.delete()

            logger.log(f"User {request.user} deleted supply: {supply_name} (ID: {supply_id}).")
            return redirect("supplies_list")

        except SupplyDeleteException as e:
            logger.log(f"Supply delete error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("supplies_list")
        except Exception as e:
            logger.log(f"Unexpected error during supply deletion: {e}")
            messages.error(request, "An unexpected error occurred while deleting the supply.")
            return redirect("supplies_list")
    return redirect("supplies_list")
