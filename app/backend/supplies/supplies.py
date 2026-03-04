from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from app.exceptions.supplies.exception import (SupplyCreationException,
                                               SupplyDeleteException,
                                               SupplyEditException)
from app.logging.logging import Logger

from ..models import (DEFAULT_TEXT_MAX_LENGTH, TEXTBOX_MAX_LENGTH,
                      UNIT_INPUT_MAX_LENGTH, Supplies)

logger = Logger("app/logging/app.log")


@login_required
def supplies_list(request):
    supplies = Supplies.objects.all().order_by("-id")

    nameToSearch = request.GET.get("nameSearch")

    if nameToSearch:
        supplies = Supplies.objects.filter(name__icontains=nameToSearch)

    paginator = Paginator(supplies, 10)
    page_number = request.GET.get("page")

    # Cant do int(None).
    if page_number:
        page_number = int(page_number)

    # If none or less than 1, make it 1.
    # If it's higher than total amount of pages we have, set it to last page.
    if not page_number or page_number < 1:
        page_number = 1
    elif page_number > paginator.num_pages:
        page_number = paginator.num_pages

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    amount_to_go = 3
    backward_pages_end = max(1, page_number - amount_to_go)
    backward_pages = reversed(range(page_number - 1, backward_pages_end - 1, -1))

    forward_pages_end = min(paginator.num_pages, page_number + amount_to_go)
    forward_pages = range(page_number + 1, forward_pages_end + 1, 1)

    logger.log(f"User {request.user} viewed supplies list.")
    context = {
        "supplies": supplies,
        "max_textbox_length": TEXTBOX_MAX_LENGTH,
        "max_input_text_length": DEFAULT_TEXT_MAX_LENGTH,
        "max_input_unit_length": UNIT_INPUT_MAX_LENGTH,
        "page_obj": page_obj,
        "backward_pages": backward_pages,
        "forward_pages": forward_pages,
    }

    return render(request, "app/supplies_list.html", context)


@login_required
def add_supplies(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            supply_category = request.POST.get("supply_category")
            quantity = request.POST.get("quantity")
            # Optional fields
            unit = request.POST.get("unit") or None
            last_restocked = request.POST.get("last_restocked") or None
            minimum_required = request.POST.get("minimum_required") or None
            cost_per_unit = request.POST.get("cost_per_unit") or None
            procurement_date = request.POST.get("procurement_date") or None
            notes = request.POST.get("notes") or None

            # Mandatory fields.
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
                if not value:
                    raise SupplyCreationException(f"Missing {key} for supply.")

            inputs_given_list = [
                (default_text_inputs_given, DEFAULT_TEXT_MAX_LENGTH),
                (unit_inputs_given, UNIT_INPUT_MAX_LENGTH),
                (textbox_inputs_given, TEXTBOX_MAX_LENGTH),
            ]

            # check length if the optional field was actually provided.
            for input_given, max_length in inputs_given_list:
                for key, value in input_given.items():
                    if value and len(value) > max_length:
                        raise SupplyCreationException(
                            f"Supply {key} input must be less or equal to {max_length} characters."
                        )

            Supplies.objects.create(
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

            logger.log(f"User {request.user} added supply: {name}")
            return redirect("supplies_list")

        except SupplyCreationException as e:
            logger.log(f"Supply creation error by {request.user}: {e}")
            supplies = Supplies.objects.all()
            return render(
                request,
                "app/supplies_list.html",
                {"supplies": supplies, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during supply creation: {e}")
            supplies = Supplies.objects.all()
            return render(
                request,
                "app/supplies_list.html",
                {
                    "supplies": supplies,
                    "error": "An unexpected error occurred while adding the supply.",
                },
            )
    return redirect("supplies_list")


@login_required
def edit_supplies(request):
    if request.method == "POST":
        try:
            try:
                supply = get_object_or_404(Supplies, id=request.POST.get("id"))
            except Http404:
                raise SupplyEditException("Supply not found.")

            supply.name = request.POST.get("name")
            supply.category = request.POST.get("supply_category")
            supply.quantity = request.POST.get("quantity")
            # Optional fields
            supply.unit = request.POST.get("unit") or None
            supply.last_restocked = request.POST.get("last_restocked") or None
            supply.minimum_required = request.POST.get("minimum_required") or None
            supply.cost_per_unit = request.POST.get("cost_per_unit") or None
            supply.procurement_date = request.POST.get("procurement_date") or None
            supply.notes = request.POST.get("notes") or None

            # Mandatory fields.
            required_inputs = {
                "name": supply.name,
                "supply_category": supply.category,
                "quantity": supply.quantity,
            }

            default_text_inputs_given = {
                "name": supply.name,
                "supply_category": supply.category,
            }

            unit_inputs_given = {
                "unit": supply.unit,
            }

            textbox_inputs_given = {
                "notes": supply.notes,
            }

            # Raise an error if mandatory field is missing.
            for key, value in required_inputs.items():
                if not value:
                    raise SupplyEditException(f"Missing {key} for supply.")

            inputs_given_list = [
                (default_text_inputs_given, DEFAULT_TEXT_MAX_LENGTH),
                (unit_inputs_given, UNIT_INPUT_MAX_LENGTH),
                (textbox_inputs_given, TEXTBOX_MAX_LENGTH),
            ]

            # check length if the optional field was actually provided.
            for input_given, max_length in inputs_given_list:
                for key, value in input_given.items():
                    if value and len(value) > max_length:
                        raise SupplyEditException(
                            f"Supply {key} input must be less or equal to {max_length} characters."
                        )

            supply.save()

            logger.log(f"User {request.user} edited supply: {supply.name}")
            return redirect("supplies_list")

        except SupplyEditException as e:
            logger.log(f"Supply edit error by {request.user}: {e}")
            supplies = Supplies.objects.all()
            return render(
                request,
                "app/supplies_list.html",
                {"supplies": supplies, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during supply edit: {e}")
            supplies = Supplies.objects.all()
            return render(
                request,
                "app/supplies_list.html",
                {
                    "supplies": supplies,
                    "error": "An unexpected error occurred while editing the supply.",
                },
            )
    return redirect("supplies_list")


@login_required
def delete_supplies(request):
    if request.method == "POST":
        try:
            try:
                supply = get_object_or_404(Supplies, id=request.POST.get("id"))
            except Http404:
                raise SupplyDeleteException("Supply not found.")

            supply_name = supply.name
            supply.delete()

            logger.log(f"User {request.user} deleted supply: {supply_name}")
            return redirect("supplies_list")

        except SupplyDeleteException as e:
            logger.log(f"Supply delete error by {request.user}: {e}")
            supplies = Supplies.objects.all()
            return render(
                request,
                "app/supplies_list.html",
                {"supplies": supplies, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during supply deletion: {e}")
            supplies = Supplies.objects.all()
            return render(
                request,
                "app/supplies_list.html",
                {
                    "supplies": supplies,
                    "error": "An unexpected error occurred while deleting the supply.",
                },
            )
    return redirect("supplies_list")
