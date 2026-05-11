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
from ..forms import SuppliesSearchForm

logger = Logger("app/logging/app.log")

@login_required
def supplies_list(request):
    form = SuppliesSearchForm(request.GET)

    supplies = Supplies.objects.all().order_by("-id")

    nameToSearch = request.GET.get("firstNameSearch")

    active_filters = []

    if form.is_valid():
        data = form.cleaned_data

        if data.get('id'):
            supplies = Supplies.objects.filter(id=data['id'])
            active_filters.append(f"ID: {str(data['id'])}")
        if data.get('name'):
            supplies = Supplies.objects.filter(name__icontains=data['name'])
            active_filters.append(f"Name: {str(data['name'])}")
        if data.get('category'):
            supplies = Supplies.objects.filter(category__icontains=data['category'])
            active_filters.append(f"Category: {str(data['category'])}")
        if data.get('min_qty'):
            supplies = Supplies.objects.filter(quantity__gte=data['min_qty'])
            active_filters.append(f"Min Qty: {str(data['min_qty'])}")
        if data.get('max_qty'):
            supplies = Supplies.objects.filter(quantity__lte=data['max_qty'])
            active_filters.append(f"Max Qty: {str(data['max_qty'])}")
        if data.get('unit'):
            supplies = Supplies.objects.filter(unit__icontains=data['unit'])
            active_filters.append(f"Unit: {str(data['unit'])}")
        if data.get('minimum_required'):
            supplies = Supplies.objects.filter(minimum_required__gte=data['minimum_required'])
            active_filters.append(f"Minimum Required: {str(data['minimum_required'])}")
        if data.get('cost_per_unit'):
            supplies = Supplies.objects.filter(cost_per_unit=data['cost_per_unit'])
            active_filters.append(f"Cost Per Unit: {str(data['cost_per_unit'])}")
        if data.get('last_restocked'):
            supplies = Supplies.objects.filter(last_restocked=data['last_restocked'])
            active_filters.append(f"Last Restocked: {str(data['last_restocked'])}")
        if data.get('procurement_date'):
            supplies = Supplies.objects.filter(last_restocked=data['procurement_date'])
            active_filters.append(f"Procurement Date: {str(data['procurement_date'])}")

    if nameToSearch:
        supplies = Supplies.objects.filter(name__icontains=nameToSearch)
        active_filters.append(f"Name: {nameToSearch}")


    # FOR PAGINATION
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

    category_given = ["Supply","supply","supplies"]
    fields_given = ["ID","Name","Category","Quantity","Unit","Last Restocked","Minimum Required","Cost Per Unit","Procurement Date","Notes","Actions"]
    object_attributes_given = ['id','name','category','quantity','unit','last_restocked','minimum_required','cost_per_unit','procurement_date']

    logger.log(f"User {request.user} viewed supplies list.")
    context = {
        'form':form,
        "supplies": supplies,
        "category_given": category_given,
        "fields_given": fields_given,
        "object_attributes_given": object_attributes_given,
        "search_filters_applied":active_filters,
        "list_url_given": 'supplies_list',
        "add_url_given": 'add_supplies',
        "edit_url_given": 'edit_supplies',
        "delete_url_given": 'delete_supplies',
        "page_obj": page_obj,
        "backward_pages": backward_pages,
        "forward_pages": forward_pages,
        "max_textbox_length": TEXTBOX_MAX_LENGTH,
        "max_input_text_length": DEFAULT_TEXT_MAX_LENGTH,
        "max_input_unit_length": UNIT_INPUT_MAX_LENGTH,
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
