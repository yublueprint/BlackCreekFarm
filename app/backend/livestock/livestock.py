from django.contrib.auth.decorators import login_required
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
    livestock = Livestock.objects.all()
    logger.log(f"User {request.user} viewed livestock list.")
    return render(request, "app/livestock_list.html", {"livestock": livestock})


@login_required
def add_livestock(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            breed = request.POST.get("breed")
            age = request.POST.get("age")
            weight = request.POST.get("weight")
            health_status = request.POST.get("health_status")
            purchase_price = request.POST.get("purchase_price")
            current_value = request.POST.get("current_value")
            next_vaccination_date = request.POST.get("next_vaccination_date")
            notes = request.POST.get("notes")

            if not name or not breed:
                raise LivestockCreationException("Both name and breed are required.")

            Livestock.objects.create(
                name=name,
                breed=breed,
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
            animal.breed = request.POST.get("breed", animal.breed)
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
            animal.notes = request.POST.get("notes", animal.notes)

            if not animal.name or not animal.breed:
                raise LivestockEditException(
                    "Name and breed are required to update livestock."
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
