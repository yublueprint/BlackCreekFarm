from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from app.exceptions.livestock.exception import (LivestockCreationException,
                                                LivestockDeleteException,
                                                LivestockEditException)
from app.logging.logging import Logger

from ..models import Livestock

logger = Logger("app/logging/app.log")


@login_required
def livestock_list(request):
    livestock = Livestock.objects.all().order_by("-id")

    nameToSearch = request.GET.get("nameSearch")

    if nameToSearch:
        livestock = Livestock.objects.filter(name__icontains=nameToSearch)

    paginator = Paginator(livestock, 10)
    page_number = request.GET.get("page")

    if page_number:
        page_number = int(page_number)

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

    logger.log(f"User {request.user} viewed livestock list.")
    context = {
        "livestock": livestock,
        "page_obj": page_obj,
        "backward_pages": backward_pages,
        "forward_pages": forward_pages,
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
