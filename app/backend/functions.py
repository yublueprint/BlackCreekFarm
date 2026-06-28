from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from app.logging.logging import Logger

# Initialize application logger
logger = Logger("app/logging/app.log")


def paginationFunction(objects, page_number=1, num_per_page=10):
    # FOR PAGINATION
    paginator = Paginator(objects, num_per_page)

    try:
        # Cant do int(None).
        if page_number:
            page_number = int(page_number)

        # If none or less than 1, make it 1.
        # If it's higher than total amount of pages we have, set it to last page.
        if not page_number or page_number < 1:
            page_number = 1
        elif page_number > paginator.num_pages:
            page_number = paginator.num_pages
    except ValueError as e:
        logger.log(
            f"Invalid value gotten for page number ({page_number}). Page number automatically set to 1. Error is: {e}"
        )
        page_number = 1
    except Exception as e:
        logger.log(
            f"An unexpected error has occured while attempting to get page number ({page_number}). Page number automatically set to 1. Error is: {e}"
        )
        page_number = 1

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

    return page_obj, backward_pages, forward_pages, page_number


def editStockNameChange(old_name, new_name):
    if old_name != new_name:
        return f"to {new_name}"
    else:
        return ""
