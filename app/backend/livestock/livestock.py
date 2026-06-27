from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from app.exceptions.livestock.exception import (LivestockCreationException,
                                                LivestockDeleteException,
                                                LivestockEditException)
from app.logging.logging import Logger

from ..forms import LivestockSearchForm
from ..functions import editStockNameChange, paginationFunction
from ..models import (DEFAULT_TEXT_MAX_LENGTH, TEXTBOX_MAX_LENGTH,
                      UNIT_INPUT_MAX_LENGTH, Livestock)

logger = Logger("app/logging/app.log")


def get_properties(request, ExceptionToUse: Exception):
    """
    Gets properties of livestock and validates the inputs.
    """
    # Mandatory fields.
    name = (request.POST.get("name") or "").strip() or "Unknown"
    type = (request.POST.get("type") or "").strip() or "Unknown"
    # Optional fields.
    age = request.POST.get("age") or None
    weight = request.POST.get("weight") or None
    health_status = (request.POST.get("health_status") or "").strip() or "Unknown"
    purchase_price = request.POST.get("purchase_price") or None
    current_value = request.POST.get("current_value") or None
    next_vaccination_date = request.POST.get("next_vaccination_date") or None
    notes = request.POST.get("notes") or ""

    required_inputs = {
        "name": name,
        "type": type,
    }

    default_text_inputs_given = {
        "name": name,
        "type": type,
        "health_status": health_status,
    }

    unit_inputs_given = {
        "age": age,
        "weight": weight,
        "purchase_price": purchase_price,
        "current_value": current_value,
    }

    textbox_inputs_given = {
        "notes": notes,
    }

    # Raise an error if mandatory fields are missing.
    for key, value in required_inputs.items():
        if value is None:
            raise ExceptionToUse(f"Missing {key} for livestock.")

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
                    f"Livestock {key} input must be less or equal to {max_length} characters."
                )

    return (
        name,
        type,
        age,
        weight,
        health_status,
        purchase_price,
        current_value,
        next_vaccination_date,
        notes,
    )


def search_filtering(form):
    livestock = Livestock.objects.all().order_by("-id")
    active_filters = []

    if form.is_valid():
        data = form.cleaned_data

        # ID
        if data.get("id"):
            livestock = livestock.filter(id=data["id"])
            active_filters.append(f"ID: {str(data['id'])}")
        # NAME
        if data.get("name"):
            livestock = livestock.filter(name__icontains=data["name"])
            active_filters.append(f"Name: {str(data['name'])}")
        # TYPE
        if data.get("type"):
            livestock = livestock.filter(type__icontains=data["type"])
            active_filters.append(f"Type: {str(data['type'])}")
        # AGE
        if data.get("age_mode"):
            if data.get("age_mode") != "all":
                if data.get("min_age") is not None:
                    livestock = livestock.filter(age__gte=data["min_age"])
                    active_filters.append(f"Min Age: {str(data['min_age'])}")
                if data.get("max_age") is not None:
                    livestock = livestock.filter(age__lte=data["max_age"])
                    active_filters.append(f"Max Age: {str(data['max_age'])}")
                if data.get("age_mode") == "highest":
                    livestock = livestock.order_by("-age")
                    active_filters.append(f"Highest to Lowest Age")
                if data.get("age_mode") == "lowest":
                    livestock = livestock.order_by("age")
                    active_filters.append(f"Lowest to Highest Age")
        # WEIGHT
        if data.get("weight_mode"):
            if data.get("weight_mode") != "all":
                if data.get("min_weight") is not None:
                    livestock = livestock.filter(weight__gte=data["min_weight"])
                    active_filters.append(f"Min Weight: {str(data['min_weight'])}")
                if data.get("max_weight") is not None:
                    livestock = livestock.filter(weight__lte=data["max_weight"])
                    active_filters.append(f"Max Weight: {str(data['max_weight'])}")
                if data.get("weight_mode") == "highest":
                    livestock = livestock.order_by("-weight")
                    active_filters.append(f"Highest to Lowest Weight")
                if data.get("weight_mode") == "lowest":
                    livestock = livestock.order_by("weight")
                    active_filters.append(f"Lowest to Highest Weight")
        # HEALTH STATUS
        if data.get("health_status"):
            livestock = livestock.filter(health_status__icontains=data["health_status"])
            active_filters.append(f"Health Status: {str(data['health_status'])}")
        # PURCHASE PRICE
        if data.get("purchase_price_mode"):
            if data.get("purchase_price_mode") != "all":
                if data.get("min_purchase_price") is not None:
                    livestock = livestock.filter(
                        purchase_price__gte=data["min_purchase_price"]
                    )
                    active_filters.append(
                        f"Min Purchase Price: {str(data['min_purchase_price'])}"
                    )
                if data.get("max_purchase_price") is not None:
                    livestock = livestock.filter(
                        purchase_price__lte=data["max_purchase_price"]
                    )
                    active_filters.append(
                        f"Max Purchase Price: {str(data['max_purchase_price'])}"
                    )
                if data.get("purchase_price_mode") == "highest":
                    livestock = livestock.order_by("-purchase_price")
                    active_filters.append(f"Highest to Lowest Purchase Price")
                if data.get("purchase_price_mode") == "lowest":
                    livestock = livestock.order_by("purchase_price")
                    active_filters.append(f"Lowest to Highest Purchase Price")
        # CURRENT VALUE
        if data.get("current_value_mode"):
            if data.get("current_value_mode") != "all":
                if data.get("min_current_value") is not None:
                    livestock = livestock.filter(
                        current_value__gte=data["min_current_value"]
                    )
                    active_filters.append(
                        f"Min Current Value: {str(data['min_current_value'])}"
                    )
                if data.get("max_current_value") is not None:
                    livestock = livestock.filter(
                        current_value__lte=data["max_current_value"]
                    )
                    active_filters.append(
                        f"Max Current Value: {str(data['max_current_value'])}"
                    )
                if data.get("current_value_mode") == "highest":
                    livestock = livestock.order_by("-current_value")
                    active_filters.append(f"Highest to Lowest Current Value")
                if data.get("current_value_mode") == "lowest":
                    livestock = livestock.order_by("current_value")
                    active_filters.append(f"Lowest to Highest Current Value")
        # NEXT VACCINATION DATE
        if data.get("next_vaccination_mode"):
            if data.get("next_vaccination_mode") != "all":
                if data.get("min_next_vaccination") is not None:
                    livestock = livestock.filter(
                        next_vaccination_date__gte=data["min_next_vaccination"]
                    )
                    active_filters.append(
                        f"Min Next Vaccination: {str(data['min_next_vaccination'])}"
                    )
                if data.get("max_next_vaccination") is not None:
                    livestock = livestock.filter(
                        next_vaccination_date__lte=data["max_next_vaccination"]
                    )
                    active_filters.append(
                        f"Max Next Vaccination: {str(data['max_next_vaccination'])}"
                    )
                if data.get("next_vaccination_mode") == "highest":
                    livestock = livestock.order_by("-next_vaccination_date")
                    active_filters.append(f"Highest to Lowest Next Vaccination Date")
                if data.get("next_vaccination_mode") == "lowest":
                    livestock = livestock.order_by("next_vaccination_date")
                    active_filters.append(f"Lowest to Highest Next Vaccination Date")
    return active_filters, livestock


@login_required
def livestock_list(request):
    # FOR SEARCH FILTERING.
    form = LivestockSearchForm(request.GET)
    active_filters, livestock = search_filtering(form)

    # FOR PAGINATION.
    page_number = request.GET.get("page")
    page_obj, backward_pages, forward_pages, page_number = paginationFunction(
        livestock, page_number, 10
    )

    context = {
        "form": form,
        "search_filters_applied": active_filters,
        "list_url_given": "livestock_list",
        "add_url_given": "add_livestock",
        "edit_url_given": "edit_livestock",
        "delete_url_given": "delete_livestock",
        "page_obj": page_obj,
        "backward_pages": backward_pages,
        "forward_pages": forward_pages,
        "max_textbox_length": TEXTBOX_MAX_LENGTH,
        "max_input_text_length": DEFAULT_TEXT_MAX_LENGTH,
        "max_input_unit_length": UNIT_INPUT_MAX_LENGTH,
    }

    logger.log(f"User {request.user} viewed livestock list (page {page_number}).")
    return render(request, "app/livestock_list.html", context)


@login_required
def add_livestock(request):
    if request.method == "POST":
        try:
            (
                name,
                type,
                age,
                weight,
                health_status,
                purchase_price,
                current_value,
                next_vaccination_date,
                notes,
            ) = get_properties(request, LivestockCreationException)

            livestock = Livestock.objects.create(
                name=name,
                type=type,
                age=age,
                weight=weight,
                health_status=health_status,
                purchase_price=purchase_price,
                current_value=current_value,
                next_vaccination_date=next_vaccination_date,
                notes=notes,
            )

            logger.log(
                f"User {request.user} added livestock: {name} (ID: {livestock.id})."
            )
            return redirect("livestock_list")

        except LivestockCreationException as e:
            logger.log(f"Livestock creation error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("livestock_list")
        except Exception as e:
            logger.log(f"Unexpected error during livestock creation: {e}")
            messages.error(
                request, "An unexpected error occurred while adding the livestock."
            )
            return redirect("livestock_list")
    return redirect("livestock_list")


@login_required
def edit_livestock(request):
    if request.method == "POST":
        try:
            try:
                animal = get_object_or_404(Livestock, id=request.POST.get("id"))
            except Http404:
                raise LivestockEditException("Livestock not found.")

            old_name = animal.name

            (
                animal.name,
                animal.type,
                animal.age,
                animal.weight,
                animal.health_status,
                animal.purchase_price,
                animal.current_value,
                animal.next_vaccination_date,
                animal.notes,
            ) = get_properties(request, LivestockEditException)

            animal.save()

            name_change_msg = editStockNameChange(old_name, animal.name)

            logger.log(
                f"User {request.user} edited livestock: {old_name} {name_change_msg} (ID: {animal.id})."
            )
            return redirect("livestock_list")

        except LivestockEditException as e:
            logger.log(f"Livestock edit error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("livestock_list")
        except Exception as e:
            logger.log(f"Unexpected error during livestock edit: {e}")
            messages.error(
                request, "An unexpected error occurred while editing the livestock."
            )
            return redirect("livestock_list")
    return redirect("livestock_list")


@login_required
def delete_livestock(request):
    if request.method == "POST":
        try:
            try:
                animal = get_object_or_404(Livestock, id=request.POST.get("id"))
            except Http404:
                raise LivestockDeleteException("Livestock not found.")

            animal_name = animal.name or "Unknown"
            animal_id = animal.id or -1
            animal.delete()

            logger.log(
                f"User {request.user} deleted livestock: {animal_name} (ID: {animal_id})."
            )
            return redirect("livestock_list")

        except LivestockDeleteException as e:
            logger.log(f"Livestock delete error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("livestock_list")
        except Exception as e:
            logger.log(f"Unexpected error during livestock deletion: {e}")
            messages.error(
                request, "An unexpected error occurred while deleting the livestock."
            )
            return redirect("livestock_list")
    return redirect("livestock_list")
