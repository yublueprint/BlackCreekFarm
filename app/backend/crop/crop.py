from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from app.exceptions.crop.exception import (CropCreationException,
                                           CropDeleteException,
                                           CropEditException)
from app.logging.logging import Logger

from ..forms import CropSearchForm
from ..functions import editStockNameChange, paginationFunction
from ..models import (DEFAULT_TEXT_MAX_LENGTH, TEXTBOX_MAX_LENGTH,
                      UNIT_INPUT_MAX_LENGTH, Crop)

logger = Logger("app/logging/app.log")


def get_properties(request, ExceptionToUse: Exception):
    """
    Gets properties of crop and validates the inputs.
    """
    # Mandatory fields.
    name = (request.POST.get("name") or "").strip() or "Unknown"
    crop_type = (request.POST.get("crop_type") or "").strip() or "Unknown"
    # Optional fields.
    planting_date = request.POST.get("planting_date") or None
    harvest_date = request.POST.get("harvest_date") or None
    expected_yield = request.POST.get("expected_yield") or None
    yield_efficiency = request.POST.get("yield_efficiency") or None
    water_usage_liters = request.POST.get("water_usage_liters") or None
    next_checkup = request.POST.get("next_checkup") or None
    region = (request.POST.get("region") or "").strip() or "Unknown"
    notes = request.POST.get("notes") or ""

    required_inputs = {
        "name": name,
        "crop_type": crop_type,
    }

    default_text_inputs_given = {
        "name": name,
        "crop_type": crop_type,
        "region": region,
    }

    unit_inputs_given = {
        "expected_yield": expected_yield,
        "yield_efficiency": yield_efficiency,
        "water_usage_liters": water_usage_liters,
    }

    textbox_inputs_given = {
        "notes": notes,
    }

    # Raise an error if mandatory fields are missing.
    for key, value in required_inputs.items():
        if value is None:
            raise ExceptionToUse(f"Missing {key} for crop.")

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
                    f"Crop {key} input must be less or equal to {max_length} characters."
                )

    return (
        name,
        crop_type,
        planting_date,
        harvest_date,
        expected_yield,
        yield_efficiency,
        water_usage_liters,
        next_checkup,
        region,
        notes,
    )


def search_filtering(form):
    crops = Crop.objects.all().order_by("-id")
    active_filters = []

    if form.is_valid():
        data = form.cleaned_data

        if data.get("id"):
            crops = crops.filter(id=data["id"])
            active_filters.append(f"ID: {str(data['id'])}")
        if data.get("name"):
            crops = crops.filter(name__icontains=data["name"])
            active_filters.append(f"Name: {str(data['name'])}")
        if data.get("crop_type"):
            crops = crops.filter(crop_type__icontains=data["crop_type"])
            active_filters.append(f"Crop Type: {str(data['crop_type'])}")
        if data.get("planting_date_mode"):
            if data.get("planting_date_mode") == "range":
                if data.get("min_planting_date") is not None:
                    crops = crops.filter(planting_date__gte=data["min_planting_date"])
                    active_filters.append(
                        f"Min Planting Date: {str(data['min_planting_date'])}"
                    )
                if data.get("max_planting_date") is not None:
                    crops = crops.filter(planting_date__lte=data["max_planting_date"])
                    active_filters.append(
                        f"Max Planting Date: {str(data['max_planting_date'])}"
                    )
                if data.get("planting_date_mode") == "highest":
                    crops = crops.order_by("-planting_date")
                    active_filters.append(f"Highest to Lowest Planting Date")
                if data.get("planting_date_mode") == "lowest":
                    crops = crops.order_by("planting_date")
                    active_filters.append(f"Lowest to Highest Planting Date")
        if data.get("harvest_date_mode"):
            if data.get("harvest_date_mode") == "range":
                if data.get("min_harvest_date") is not None:
                    crops = crops.filter(harvest_date__gte=data["min_harvest_date"])
                    active_filters.append(
                        f"Min Harvest Date: {str(data['min_harvest_date'])}"
                    )
                if data.get("max_harvest_date") is not None:
                    crops = crops.filter(harvest_date__lte=data["max_harvest_date"])
                    active_filters.append(
                        f"Max Harvest Date: {str(data['max_harvest_date'])}"
                    )
                if data.get("harvest_date_mode") == "highest":
                    crops = crops.order_by("-harvest_date")
                    active_filters.append(f"Highest to Lowest Harvest Date")
                if data.get("harvest_date_mode") == "lowest":
                    crops = crops.order_by("harvest_date")
                    active_filters.append(f"Lowest to Highest Harvest Date")
        if data.get("expected_yield_mode"):
            if data.get("expected_yield_mode") == "range":
                if data.get("min_expected_yield") is not None:
                    crops = crops.filter(expected_yield__gte=data["min_expected_yield"])
                    active_filters.append(
                        f"Min Expected Yield: {str(data['min_expected_yield'])}"
                    )
                if data.get("max_expected_yield") is not None:
                    crops = crops.filter(expected_yield__lte=data["max_expected_yield"])
                    active_filters.append(
                        f"Max Expected Yield: {str(data['max_expected_yield'])}"
                    )
                if data.get("expected_yield_mode") == "highest":
                    crops = crops.order_by("-expected_yield")
                    active_filters.append(f"Highest to Lowest Expected Yield")
                if data.get("expected_yield_mode") == "lowest":
                    crops = crops.order_by("expected_yield")
                    active_filters.append(f"Lowest to Highest Expected Yield")
        if data.get("yield_efficiency_mode"):
            if data.get("yield_efficiency_mode") == "range":
                if data.get("min_yield_efficiency") is not None:
                    crops = crops.filter(
                        yield_efficiency__gte=data["min_yield_efficiency"]
                    )
                    active_filters.append(
                        f"Min Yield Efficiency: {str(data['min_yield_efficiency'])}"
                    )
                if data.get("max_yield_efficiency") is not None:
                    crops = crops.filter(
                        yield_efficiency__lte=data["max_yield_efficiency"]
                    )
                    active_filters.append(
                        f"Max Yield Efficiency: {str(data['max_yield_efficiency'])}"
                    )
                if data.get("yield_efficiency_mode") == "highest":
                    crops = crops.order_by("-yield_efficiency")
                    active_filters.append(f"Highest to Lowest Yield Efficiency")
                if data.get("yield_efficiency_mode") == "lowest":
                    crops = crops.order_by("yield_efficiency")
                    active_filters.append(f"Lowest to Highest Yield Efficiency")
        if data.get("water_usage_mode"):
            if data.get("water_usage_mode") == "range":
                if data.get("min_water_usage") is not None:
                    crops = crops.filter(
                        water_usage_liters__gte=data["min_water_usage"]
                    )
                    active_filters.append(
                        f"Min Water Usage: {str(data['min_water_usage'])}"
                    )
                if data.get("max_water_usage") is not None:
                    crops = crops.filter(
                        water_usage_liters__lte=data["max_water_usage"]
                    )
                    active_filters.append(
                        f"Max Water Usage: {str(data['max_water_usage'])}"
                    )
                if data.get("water_usage_mode") == "highest":
                    crops = crops.order_by("-water_usage")
                    active_filters.append(f"Highest to Lowest Water Usage")
                if data.get("water_usage_mode") == "lowest":
                    crops = crops.order_by("water_usage")
                    active_filters.append(f"Lowest to Highest Water Usage")
        if data.get("next_checkup_mode"):
            if data.get("next_checkup_mode") == "range":
                if data.get("min_next_checkup") is not None:
                    crops = crops.filter(next_checkup__gte=data["min_next_checkup"])
                    active_filters.append(
                        f"Min Next Checkup: {str(data['min_next_checkup'])}"
                    )
                if data.get("max_next_checkup") is not None:
                    crops = crops.filter(next_checkup__lte=data["max_next_checkup"])
                    active_filters.append(
                        f"Max Next Checkup: {str(data['max_next_checkup'])}"
                    )
                if data.get("next_checkup_mode") == "highest":
                    crops = crops.order_by("-next_checkup")
                    active_filters.append(f"Highest to Lowest Next Checkup")
                if data.get("next_checkup_mode") == "lowest":
                    crops = crops.order_by("next_checkup")
                    active_filters.append(f"Lowest to Highest Next Checkup")
        if data.get("region"):
            crops = crops.filter(region__icontains=data["region"])
            active_filters.append(f"Region: {str(data['region'])}")
    return active_filters, crops


@login_required
def crop_list(request, id=None):
    try:
        # FOR SEARCH FILTERING.
        form = CropSearchForm(request.GET)
        active_filters, crops = search_filtering(form)

        # If ID was given in URL. Ex: supplies/id/<int>
        try:
            if (id):
                crop = Crop.objects.filter(id=id)

                if not crop.exists():
                    raise Exception(f"Crop of ID {id} does not exist.")
        except Exception as e:
            logger.log(f"Error in crops view by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("crop_list")

        # FOR PAGINATION.
        page_number = request.GET.get("page")
        page_obj, backward_pages, forward_pages, page_number = paginationFunction(
            crops, page_number, 10
        )

        context = {
            "form": form,
            "search_filters_applied": active_filters,
            "list_url_given": "crop_list",
            "add_url_given": "add_crop",
            "edit_url_given": "edit_crop",
            "delete_url_given": "delete_crop",
            "page_obj": page_obj,
            "backward_pages": backward_pages,
            "forward_pages": forward_pages,
            "max_textbox_length": TEXTBOX_MAX_LENGTH,
            "max_input_text_length": DEFAULT_TEXT_MAX_LENGTH,
            "max_input_unit_length": UNIT_INPUT_MAX_LENGTH,
        }

        logger.log(f"User {request.user} viewed crop list (page {page_number}).")
        return render(request, "app/crop_list.html", context)
    except Exception as e:
        logger.log(f"Error in crops view by {request.user}: {e}")
        messages.error(request, str(e))
        return redirect("error_page")


@login_required
def add_crop(request):
    if request.method == "POST":
        try:
            (
                name,
                crop_type,
                planting_date,
                harvest_date,
                expected_yield,
                yield_efficiency,
                water_usage_liters,
                next_checkup,
                region,
                notes,
            ) = get_properties(request, CropCreationException)

            crop = Crop.objects.create(
                name=name,
                crop_type=crop_type,
                planting_date=planting_date,
                harvest_date=harvest_date if harvest_date else None,
                expected_yield=float(expected_yield) if expected_yield else 0,
                yield_efficiency=float(yield_efficiency) if yield_efficiency else 0,
                water_usage_liters=(
                    float(water_usage_liters) if water_usage_liters else 0
                ),
                next_checkup=next_checkup if next_checkup else None,
                region=region,
                notes=notes,
            )

            logger.log(f"User {request.user} added crop: {name} (ID: {crop.id}).")
            return redirect("crop_list")

        except CropCreationException as e:
            logger.log(f"Crop creation error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("crop_list")
        except ValueError as e:
            logger.log(f"Value error during crop creation by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("crop_list")
        except Exception as e:
            logger.log(f"Unexpected error during crop creation: {e}")
            messages.error(
                request, "An unexpected error occurred while adding the crop."
            )
            return redirect("crop_list")
    return redirect("crop_list")


@login_required
def edit_crop(request):
    if request.method == "POST":
        try:
            try:
                crop = get_object_or_404(Crop, id=request.POST.get("id"))
            except Http404:
                raise CropEditException("Crop not found.")

            old_name = crop.name

            (
                crop.name,
                crop.crop_type,
                crop.planting_date,
                crop.harvest_date,
                crop.expected_yield,
                crop.yield_efficiency,
                crop.water_usage_liters,
                crop.next_checkup,
                crop.region,
                crop.notes,
            ) = get_properties(request, CropEditException)

            crop.save()

            name_change_msg = editStockNameChange(old_name, crop.name)

            logger.log(
                f"User {request.user} edited crop: {old_name} {name_change_msg} (ID: {crop.id})."
            )
            return redirect("crop_list")

        except CropEditException as e:
            logger.log(f"Crop edit error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("crop_list")
        except Exception as e:
            logger.log(f"Unexpected error during crop edit: {e}")
            messages.error(
                request, "An unexpected error occurred while editing the crop."
            )
            return redirect("crop_list")
    return redirect("crop_list")


@login_required
def delete_crop(request):
    if request.method == "POST":
        try:
            try:
                crop = get_object_or_404(Crop, id=request.POST.get("id"))
            except Http404:
                raise CropDeleteException("Crop not found.")

            crop_name = crop.name or "Unknown"
            crop_id = crop.id or -1
            crop.delete()

            logger.log(
                f"User {request.user} deleted crop: {crop_name} (ID: {crop_id})."
            )
            return redirect("crop_list")

        except CropDeleteException as e:
            logger.log(f"Crop delete error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("crop_list")
        except Exception as e:
            logger.log(f"Unexpected error during crop deletion: {e}")
            messages.error(
                request, "An unexpected error occurred while deleting the crop."
            )
            return redirect("crop_list")
    return redirect("crop_list")
