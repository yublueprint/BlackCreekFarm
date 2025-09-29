from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404

from app.exceptions.supplies.exception import (
    SupplyCreationException,
    SupplyEditException,
    SupplyDeleteException,
)
from app.logging.logging import Logger
from ..models import Supplies

logger = Logger("app/logging/app.log")


@login_required
def supplies_list(request):
    supplies = Supplies.objects.all()
    logger.log(f"User {request.user} viewed supplies list.")
    return render(request, "app/supplies_list.html", {"supplies": supplies})


@login_required
def add_supplies(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            supply_type = request.POST.get("type")  # avoid shadowing builtin `type`
            quantity = request.POST.get("quantity")
            unit = request.POST.get("unit")

            if not name or not supply_type:
                raise SupplyCreationException("Missing name or type for supply.")

            Supplies.objects.create(
                name=name,
                type=supply_type,
                quantity=quantity,
                unit=unit,
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
            supply.type = request.POST.get("type")
            supply.quantity = request.POST.get("quantity")
            supply.unit = request.POST.get("unit")

            if not supply.name or not supply.type:
                raise SupplyEditException("Name and type are required to update supply.")

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
