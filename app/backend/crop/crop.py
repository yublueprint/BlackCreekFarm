from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render

from app.exceptions.crop.exception import (
    CropCreationException,
    CropDeleteException,
    CropEditException,
)
from app.logging.logging import Logger

from ..models import Crop

logger = Logger("app/logging/app.log")


@login_required
def crop_list(request):
    crops_list = Crop.objects.all().order_by("-planting_date")

    # Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(crops_list, 10)

    try:
        crops = paginator.page(page)
    except PageNotAnInteger:
        crops = paginator.page(1)
    except EmptyPage:
        crops = paginator.page(paginator.num_pages)

    logger.log(f"User {request.user} viewed crop list (page {page}).")
    return render(request, "app/crop_list.html", {"crops": crops})


@login_required
def add_crop(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            crop_type = request.POST.get("crop_type")
            planting_date = request.POST.get("planting_date")
            harvest_date = request.POST.get("harvest_date")
            expected_yield = request.POST.get("expected_yield")
            yield_efficiency = request.POST.get("yield_efficiency")
            water_usage_liters = request.POST.get("water_usage_liters")
            next_checkup = request.POST.get("next_checkup")
            region = request.POST.get("region")
            notes = request.POST.get("notes")

            # REQUIRED FIELDS (aligned with ticket)
            if not name or not crop_type or not planting_date:
                raise CropCreationException(
                    "Name, crop type, and planting date are required."
                )

            crop = Crop.objects.create(
                name=name,
                crop_type=crop_type,
                planting_date=planting_date,
                harvest_date=harvest_date if harvest_date else None,
                expected_yield=float(expected_yield) if expected_yield else 0,
                yield_efficiency=float(yield_efficiency) if yield_efficiency else 0,
                water_usage_liters=float(water_usage_liters) if water_usage_liters else 0,
                next_checkup=next_checkup if next_checkup else None,
                region=region,
                notes=notes,
            )

            logger.log(f"User {request.user} added crop: {name} (ID: {crop.id})")
            return redirect("crop_list")

        except CropCreationException as e:
            logger.log(f"Crop creation error by {request.user}: {e}")

            crops_list = Crop.objects.all().order_by("-planting_date")
            paginator = Paginator(crops_list, 10)
            crops = paginator.page(1)

            return render(
                request,
                "app/crop_list.html",
                {"crops": crops, "error": str(e)},
            )

        except ValueError as e:
            logger.log(f"Value error during crop creation by {request.user}: {e}")

            crops_list = Crop.objects.all().order_by("-planting_date")
            paginator = Paginator(crops_list, 10)
            crops = paginator.page(1)

            return render(
                request,
                "app/crop_list.html",
                {
                    "crops": crops,
                    "error": "Invalid input values. Please check numeric fields.",
                },
            )

        except Exception as e:
            logger.log(f"Unexpected error during crop creation: {e}")

            crops_list = Crop.objects.all().order_by("-planting_date")
            paginator = Paginator(crops_list, 10)
            crops = paginator.page(1)

            return render(
                request,
                "app/crop_list.html",
                {
                    "crops": crops,
                    "error": "An unexpected error occurred while adding the crop.",
                },
            )

    return redirect("crop_list")


@login_required
def edit_crop(request):
    if request.method == "POST":
        try:
            crop_id = request.POST.get("id")
            if not crop_id:
                raise CropEditException("Crop ID is required.")

            crop = get_object_or_404(Crop, id=crop_id)
            old_name = crop.name

            crop.name = request.POST.get("name")
            crop.crop_type = request.POST.get("crop_type")
            crop.planting_date = request.POST.get("planting_date")
            crop.harvest_date = request.POST.get("harvest_date")
            crop.expected_yield = request.POST.get("expected_yield")
            crop.yield_efficiency = request.POST.get("yield_efficiency")
            crop.water_usage_liters = request.POST.get("water_usage_liters")
            crop.next_checkup = request.POST.get("next_checkup")
            crop.region = request.POST.get("region")
            crop.notes = request.POST.get("notes")

            # REQUIRED FIELDS (aligned with ticket)
            if not crop.name or not crop.crop_type or not crop.planting_date:
                raise CropEditException(
                    "Name, crop type, and planting date are required."
                )

            # NUMERIC FIELDS: allow blank -> 0; invalid -> error
            try:
                crop.expected_yield = float(crop.expected_yield) if crop.expected_yield else 0
                crop.yield_efficiency = float(crop.yield_efficiency) if crop.yield_efficiency else 0
                crop.water_usage_liters = float(crop.water_usage_liters) if crop.water_usage_liters else 0
            except ValueError:
                raise CropEditException(
                    "Invalid numeric values in yield or water usage fields."
                )

            crop.harvest_date = crop.harvest_date if crop.harvest_date else None
            crop.next_checkup = crop.next_checkup if crop.next_checkup else None

            crop.save()
            logger.log(f"User {request.user} edited crop: {old_name} to {crop.name}")
            return redirect("crop_list")

        except CropEditException as e:
            logger.log(f"Crop edit error by {request.user}: {e}")

            crops_list = Crop.objects.all().order_by("-planting_date")
            paginator = Paginator(crops_list, 10)
            crops = paginator.page(1)

            return render(
                request,
                "app/crop_list.html",
                {"crops": crops, "error": str(e)},
            )

        except Exception as e:
            logger.log(f"Unexpected error during crop edit: {e}")

            crops_list = Crop.objects.all().order_by("-planting_date")
            paginator = Paginator(crops_list, 10)
            crops = paginator.page(1)

            return render(
                request,
                "app/crop_list.html",
                {
                    "crops": crops,
                    "error": "An unexpected error occurred while editing the crop.",
                },
            )

    return redirect("crop_list")


@login_required
def delete_crop(request):
    if request.method == "POST":
        try:
            crop_id = request.POST.get("id")
            if not crop_id:
                raise CropDeleteException("Crop ID is required.")

            crop = get_object_or_404(Crop, id=crop_id)

            crop_name = crop.name
            crop.delete()
            logger.log(f"User {request.user} deleted crop: {crop_name}")
            return redirect("crop_list")

        except CropDeleteException as e:
            logger.log(f"Crop delete error by {request.user}: {e}")

            crops_list = Crop.objects.all().order_by("-planting_date")
            paginator = Paginator(crops_list, 10)
            crops = paginator.page(1)

            return render(
                request,
                "app/crop_list.html",
                {"crops": crops, "error": str(e)},
            )

        except Exception as e:
            logger.log(f"Unexpected error during crop deletion: {e}")

            crops_list = Crop.objects.all().order_by("-planting_date")
            paginator = Paginator(crops_list, 10)
            crops = paginator.page(1)

            return render(
                request,
                "app/crop_list.html",
                {
                    "crops": crops,
                    "error": "An unexpected error occurred while deleting the crop.",
                },
            )

    return redirect("crop_list")