from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from app.exceptions.livestock.exception import (LivestockCreationException,
                                                LivestockDeleteException,
                                                LivestockEditException)
from app.logging.logging import Logger

from ..models import (DEFAULT_TEXT_MAX_LENGTH, TEXTBOX_MAX_LENGTH,
                      UNIT_INPUT_MAX_LENGTH, Livestock)
from ..forms import LivestockSearchForm
from ..functions import paginationFunction

logger = Logger("app/logging/app.log")


@login_required
def livestock_list(request):
    form = LivestockSearchForm(request.GET)

    livestock = Livestock.objects.all().order_by("-id")

    nameToSearch = request.GET.get("firstNameSearch")
    
    active_filters = []

    if form.is_valid():
        data = form.cleaned_data

        # ID
        if data.get('id'):
            livestock = livestock.filter(id=data['id'])
            active_filters.append(f"ID: {str(data['id'])}")
        # NAME
        if data.get('name'):
            livestock = livestock.filter(name__icontains=data['name'])
            active_filters.append(f"Name: {str(data['name'])}")
        # TYPE
        if data.get('type'):
            livestock = livestock.filter(type__icontains=data['type'])
            active_filters.append(f"Type: {str(data['type'])}")
        # AGE
        if data.get('age_mode'):
            if data.get('age_mode') == 'range':
                if data.get('min_age') is not None:
                    livestock = livestock.filter(age__gte=data['min_age'])
                    active_filters.append(f"Min Age: {str(data['min_age'])}")
                if data.get('max_age') is not None:
                    livestock = livestock.filter(age__lte=data['max_age'])
                    active_filters.append(f"Max Age: {str(data['max_age'])}")
        # WEIGHT
        if data.get('weight_mode'):
            if data.get('weight_mode') == 'range':
                if data.get('min_weight') is not None:
                    livestock = livestock.filter(weight__gte=data['min_weight'])
                    active_filters.append(f"Min Weight: {str(data['min_weight'])}")
                if data.get('max_weight') is not None:
                    livestock = livestock.filter(weight__lte=data['max_weight'])
                    active_filters.append(f"Max Weight: {str(data['max_weight'])}")
        # HEALTH STATUS
        if data.get('health_status'):
            livestock = livestock.filter(health_status__icontains=data['health_status'])
            active_filters.append(f"Health Status: {str(data['health_status'])}")
        # PURCHASE PRICE
        if data.get('purchase_price_mode'):
            if data.get('purchase_price_mode') == 'range':
                if data.get('min_purchase_price') is not None:
                    livestock = livestock.filter(purchase_price__gte=data['min_purchase_price'])
                    active_filters.append(f"Min Purchase Price: {str(data['min_purchase_price'])}")
                if data.get('max_purchase_price') is not None:
                    livestock = livestock.filter(purchase_price__lte=data['max_purchase_price'])
                    active_filters.append(f"Max Purchase Price: {str(data['max_purchase_price'])}")
        # CURRENT VALUE
        if data.get('current_value_mode'):
            if data.get('current_value_mode') == 'range':
                if data.get('min_current_value') is not None:
                    livestock = livestock.filter(current_value__gte=data['min_current_value'])
                    active_filters.append(f"Min Current Value: {str(data['min_current_value'])}")
                if data.get('max_current_value') is not None:
                    livestock = livestock.filter(current_value__lte=data['max_current_value'])
                    active_filters.append(f"Max Current Value: {str(data['max_current_value'])}")
        # NEXT VACCINATION DATE
        if data.get('next_vaccination_mode'):
            if data.get('next_vaccination_mode') == 'range':
                if data.get('min_next_vaccination') is not None:
                    livestock = livestock.filter(next_vaccination_date__gte=data['min_next_vaccination'])
                    active_filters.append(f"Min Next Vaccination: {str(data['min_next_vaccination'])}")
                if data.get('max_next_vaccination') is not None:
                    livestock = livestock.filter(next_vaccination_date__lte=data['max_next_vaccination'])
                    active_filters.append(f"Max Next Vaccination: {str(data['max_next_vaccination'])}")


    if nameToSearch:
        livestock = livestock.filter(name__icontains=nameToSearch)
        active_filters.append(f"Name: {nameToSearch}")

    # FOR PAGINATION.
    page_number = request.GET.get("page")
    page_obj, backward_pages, forward_pages = paginationFunction(livestock, page_number, 10)

    # Livestock Titles, Fields, and Properties.
    category_given = ["Livestock", "livestock", "livestock"]
    fields_given = ["ID", "Name", "Type of Animal (Species)", "Age", "Weight (kg)", "Health", "Purchase Price", "Value ($)", "Next Vaccination", "Notes", "Actions"]
    object_attributes_given = ['id', 'name', 'type', 'age', 'weight', 'health_status', 'purchase_price', 'current_value', 'next_vaccination_date']

    logger.log(f"User {request.user} viewed livestock list.")
    context = {
        'form': form,
        "livestock": livestock,
        "category_given": category_given,
        "fields_given": fields_given,
        "object_attributes_given": object_attributes_given,
        "search_filters_applied": active_filters,
        "list_url_given": 'livestock_list',
        "add_url_given": 'add_livestock',
        "edit_url_given": 'edit_livestock',
        "delete_url_given": 'delete_livestock', 
        "page_obj": page_obj,
        "backward_pages": backward_pages,
        "forward_pages": forward_pages,
        "max_textbox_length": TEXTBOX_MAX_LENGTH,
        "max_input_text_length": DEFAULT_TEXT_MAX_LENGTH,
        "max_input_unit_length": UNIT_INPUT_MAX_LENGTH,
    }

    return render(request, "app/livestock_list.html", context)


@login_required
def add_livestock(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            type = request.POST.get("type")
            age = request.POST.get("age")
            weight = request.POST.get("weight")
            health_status = request.POST.get("health_status")
            purchase_price = request.POST.get("purchase_price")
            current_value = request.POST.get("current_value")
            next_vaccination_date = request.POST.get("next_vaccination_date")
            notes = request.POST.get("notes")

            if not name or not type:
                raise LivestockCreationException("Both name and type are required.")

            Livestock.objects.create(
                name=name,
                type=type,
                age=age or 0,
                weight=weight or None,
                health_status=health_status or "Unknown",
                purchase_price=purchase_price or 0,
                current_value=current_value or 0,
                next_vaccination_date=next_vaccination_date or None,
                notes=notes or "",
            )

            logger.log(f"User {request.user} added livestock: {name}")
            return redirect("livestock_list")

        except LivestockCreationException as e:
            logger.log(f"Livestock creation error by {request.user}: {e}")
            livestock = Livestock.objects.all()
            return render(
                request,
                "app/livestock_list.html",
                {"livestock": livestock, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during livestock creation: {e}")
            livestock = Livestock.objects.all()
            return render(
                request,
                "app/livestock_list.html",
                {
                    "livestock": livestock,
                    "error": "An unexpected error occurred while adding the livestock.",
                },
            )
    return redirect("livestock_list")


@login_required
def edit_livestock(request):
    if request.method == "POST":
        try:
            try:
                animal = get_object_or_404(Livestock, id=request.POST.get("id"))
            except Http404:
                raise LivestockEditException("Livestock not found.")

            # ✅ Safe updates: preserve existing values if keys are missing
            animal.name = request.POST.get("name", animal.name)
            animal.type = request.POST.get("type", animal.type)
            animal.age = request.POST.get("age", animal.age)
            animal.weight = request.POST.get("weight", animal.weight)
            animal.health_status = request.POST.get(
                "health_status", animal.health_status
            )
            animal.purchase_price = request.POST.get(
                "purchase_price", animal.purchase_price
            )
            animal.current_value = request.POST.get(
                "current_value", animal.current_value
            )
            animal.next_vaccination_date = request.POST.get(
                "next_vaccination_date", animal.next_vaccination_date
            )
            if (len(str(animal.age)) == 0) or (animal.age == ""):
                animal.age = None
            if (len(str(animal.weight)) == 0) or (animal.weight == ""):
                animal.weight = None
            if (len(str(animal.next_vaccination_date)) == 0) or (
                animal.next_vaccination_date == ""
            ):
                animal.next_vaccination_date = None
            animal.notes = request.POST.get("notes", animal.notes)
            if (len(str(animal.purchase_price)) == 0) or (animal.purchase_price == ""):
                animal.purchase_price = 0
            if (len(str(animal.current_value)) == 0) or (animal.current_value == ""):
                animal.current_value = 0

            if not animal.name or not animal.type:
                raise LivestockEditException(
                    "Name and type are required to update livestock."
                )

            animal.save()
            logger.log(f"User {request.user} edited livestock: {animal.name}")
            return redirect("livestock_list")

        except LivestockEditException as e:
            logger.log(f"Livestock edit error by {request.user}: {e}")
            livestock = Livestock.objects.all()
            return render(
                request,
                "app/livestock_list.html",
                {"livestock": livestock, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during livestock edit: {e}")
            livestock = Livestock.objects.all()
            return render(
                request,
                "app/livestock_list.html",
                {
                    "livestock": livestock,
                    "error": "An unexpected error occurred while editing the livestock.",
                },
            )
    return redirect("livestock_list")


@login_required
def delete_livestock(request):
    if request.method == "POST":
        try:
            try:
                animal = get_object_or_404(Livestock, id=request.POST.get("id"))
            except Http404:
                raise LivestockDeleteException("Livestock not found.")

            animal_name = animal.name
            animal.delete()

            logger.log(f"User {request.user} deleted livestock: {animal_name}")
            return redirect("livestock_list")

        except LivestockDeleteException as e:
            logger.log(f"Livestock delete error by {request.user}: {e}")
            livestock = Livestock.objects.all()
            return render(
                request,
                "app/livestock_list.html",
                {"livestock": livestock, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during livestock deletion: {e}")
            livestock = Livestock.objects.all()
            return render(
                request,
                "app/livestock_list.html",
                {
                    "livestock": livestock,
                    "error": "An unexpected error occurred while deleting the livestock.",
                },
            )
    return redirect("livestock_list")
