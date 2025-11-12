from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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
        name = request.POST.get("name")
        breed = request.POST.get("breed")
        age = request.POST.get("age")
        health_status = request.POST.get("health_status")

        Livestock.objects.create(
            name=name,
            breed=breed,
            age=age,
            health_status=health_status,
        )
        logger.log(f"User {request.user} added livestock: {name}")
        return redirect("livestock_list")
    else:
        return redirect("livestock_list")

@login_required
def edit_livestock(request):
    if request.method == "POST":
        animal = get_object_or_404(Livestock, id=request.POST.get("id"))
        old_name = animal.name
        animal.name = request.POST.get("name")
        animal.breed = request.POST.get("breed")
        animal.age = request.POST.get("age")
        animal.health_status = request.POST.get("health_status")
        animal.save()
        logger.log(f"User {request.user} edited livestock: {old_name} to {animal.name}")
        return redirect("livestock_list")
    else:
        return redirect("livestock_list")

@login_required
def delete_livestock(request):
    if request.method == "POST":
        animal = get_object_or_404(Livestock, id=request.POST.get("id"))
        animal_name = animal.name
        animal.delete()
        logger.log(f"User {request.user} deleted livestock: {animal_name}")
        return redirect("livestock_list")
    else:
        return redirect("livestock_list") 