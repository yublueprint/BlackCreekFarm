import io
import os
import zipfile

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import FileResponse
from django.shortcuts import render

from app.logging.logging import Logger

logger = Logger("app/logging/app.log")


@login_required
def recent_activities_list(request):
    logger.log(f"User {request.user} viewed recent activities list.")

    recent_activities = logger.retrieve_recent_activity(5, True)
    paginator = Paginator(recent_activities, 25)
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

    context = {
        "recent_activity": recent_activities,
        "page_obj": page_obj,
        "backward_pages": backward_pages,
        "forward_pages": forward_pages,
    }

    return render(request, "app/recent_activities_list.html", context)


@login_required
def download_all_activities(request):
    logger.log(
        f"User {request.user} downloaded all activity logs from recent activities list page."
    )

    try:
        buffer = io.BytesIO()

        mod_activity_logs = logger.download_all_activity_logs()
        # print(mod_activity_logs)

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_name in mod_activity_logs:
                if os.path.exists(file_name):
                    zipf.write(file_name, arcname=file_name)

        buffer.seek(0)

        response = FileResponse(
            buffer, as_attachment=True, filename="bulk_log_download.zip"
        )
    except Exception as e:
        logger.log(f"Unexpected error during log file download: {e}")
        # response = redirect("recent_activities_list")
        context = {
            "recent_activity": logger.retrieve_recent_activity(5, True),
            "error": str(e),
        }
        response = render(request, "app/recent_activities_list.html", context)
    finally:
        return response
