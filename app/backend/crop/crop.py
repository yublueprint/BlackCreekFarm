from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from app.logging.logging import Logger 
from app.exceptions.crop.exception import CropCreationException,CropEditException,CropDeleteException

from ..models import Crop  

logger = Logger("app/logging/app.log")


@login_required
def crop_list(request):
    crops = Crop.objects.all()
    logger.log(f"User {request.user} viewed crop list.")
    return render(request, "app/crop_list.html", {"crops": crops})


@login_required
def add_crop(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            planting_date = request.POST.get("planting_date")
            harvest_date = request.POST.get("harvest_date")
            yield_estimate = request.POST.get("yield_estimate")

            if not name or not planting_date or not harvest_date or not yield_estimate:
                raise CropCreationException("All fields are required.")

            Crop.objects.create(
                name=name,
                planting_date=planting_date,
                harvest_date=harvest_date,
                yield_estimate=yield_estimate,
            ) 
            logger.log(f"User {request.user} added crop: {name}")
            return redirect("crop_list")

        except CropCreationException as e:
            logger.log(f"Crop creation error by {request.user}: {e}")
            crops = Crop.objects.all()
            return render(
                request,
                "app/crop_list.html",
                {"crops": crops, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during crop creation: {e}")
            crops = Crop.objects.all()
            return render(
                request,
                "app/crop_list.html",
                {
                    "crops": crops,
                    "error": "An unexpected error occurred while adding the crop.",
                },
            )


@login_required
def edit_crop(request):
    if request.method == "POST":
        try:
            crop = get_object_or_404(Crop, id=request.POST.get("id"))
            if not crop:
                raise CropEditException("Crop not found.")

            old_name = crop.name
            crop.name = request.POST.get("name")
            crop.planting_date = request.POST.get("planting_date")
            crop.harvest_date = request.POST.get("harvest_date")
            crop.yield_estimate = request.POST.get("yield_estimate")

            if not crop.name or not crop.planting_date or not crop.harvest_date or not crop.yield_estimate:
                raise CropEditException("All fields are required to update crop.")

            crop.save()
            logger.log(f"User {request.user} edited crop: {old_name} to {crop.name}")
            return redirect("crop_list")

        except CropEditException as e:
            logger.log(f"Crop edit error by {request.user}: {e}")
            crops = Crop.objects.all()
            return render(
                request,
                "app/crop_list.html",
                {"crops": crops, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during crop edit: {e}")
            crops = Crop.objects.all()
            return render(
                request,
                "app/crop_list.html",
                {
                    "crops": crops,
                    "error": "An unexpected error occurred while editing the crop.",
                },
            ) 


@login_required
def delete_crop(request):
    if request.method == "POST":
        try:
            crop = get_object_or_404(Crop, id=request.POST.get("id"))

            if not crop:
                raise CropDeleteException("Crop not found.") 

            crop_name = crop.name
            crop.delete()
            logger.log(f"User {request.user} deleted crop: {crop_name}")
            return redirect("crop_list")
        
        except CropDeleteException as e:
            logger.log(f"Crop delete error by {request.user}: {e}")
            crops = Crop.objects.all()
            return render(
                request,
                "app/crop_list.html",
                {"crops": crops, "error": str(e)},
            )
        except Exception as e:
            logger.log(f"Unexpected error during crop deletion: {e}")
            crops = Crop.objects.all()
            return render(
                request,
                "app/crop_list.html",
                {
                    "crops": crops,
                    "error": "An unexpected error occurred while deleting the crop.",
                },
            )

