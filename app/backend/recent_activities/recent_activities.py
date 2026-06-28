import io
import os
import zipfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import redirect, render

from app.backend.functions import paginationFunction
from app.logging.logging import Logger

logger = Logger("app/logging/app.log")


@login_required
def recent_activities_list(request):
    try:
        recent_activities = logger.retrieve_recent_activity(5, True)

        # PAGINATION
        page_number = request.GET.get("page")
        page_obj, backward_pages, forward_pages, page_number = paginationFunction(
            recent_activities, page_number, 25
        )

        context = {
            "recent_activity": recent_activities,
            "page_obj": page_obj,
            "backward_pages": backward_pages,
            "forward_pages": forward_pages,
        }

        logger.log(
            f"User {request.user} viewed recent activities list (page {page_number})."
        )
        return render(request, "app/recent_activities_list.html", context)
    except Exception as e:
        logger.log(f"Error in recent activities view by {request.user}: {e}")
        messages.error(request, str(e))
        return redirect("error_page")


@login_required
def download_all_activities(request):
    logger.log(
        f"User {request.user} downloaded all activity logs from recent activities list page."
    )

    try:
        buffer = io.BytesIO()

        mod_activity_logs = logger.download_all_activity_logs()
        # print(f"MOD ACTIVITY LOGS: {mod_activity_logs}")

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            for file_name in mod_activity_logs:
                if os.path.exists(file_name):
                    file_count = file_count + 1
                    zipf.write(
                        file_name, arcname=f"modification_activities_{file_count}.log"
                    )

        buffer.seek(0)

        response = FileResponse(
            buffer,
            as_attachment=True,
            filename="activity_logs.zip",
            content_type="application/zip",
        )
        return response
    except Exception as e:
        logger.log(f"Unexpected error during log file download: {e}")
        messages.error(
            request, "An unexpected error occurred while downloading the log files."
        )
        return redirect("recent_activities_list")
