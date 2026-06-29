from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from app.exceptions.transactions.exception import (
    TransactionCreationException, TransactionDeleteException,
    TransactionEditException)
from app.logging.logging import Logger

from ..forms import TransactionSearchForm
from ..functions import editStockNameChange, paginationFunction
from ..models import (DEFAULT_TEXT_MAX_LENGTH, TEXTBOX_MAX_LENGTH,
                      UNIT_INPUT_MAX_LENGTH, Transaction)

logger = Logger("app/logging/app.log")


def get_properties(request, ExceptionToUse: Exception):
    """
    Gets properties of transaction and validates the inputs.
    """
    # Mandatory fields.
    item_type = (request.POST.get("item_type") or "").strip() or "Unknown"
    item_id = request.POST.get("item_id") or -1
    item_name = (request.POST.get("item_name") or "").strip() or "Unknown"
    transaction_type = (request.POST.get("transaction_type") or "").strip() or "Unknown"
    quantity = request.POST.get("quantity") or -1
    date = request.POST.get("date") or None
    # Optional fields.
    notes = request.POST.get("notes") or ""

    required_inputs = {
        "item_type": item_type,
        "item_id": item_id,
        "item_name": item_name,
        "transaction_type": transaction_type,
        "quantity": quantity,
        "date": date,
    }

    default_text_inputs_given = {
        "item_type": item_type,
        "item_name": item_name,
        "transaction_type": transaction_type,
    }

    unit_inputs_given = {
        "quantity": quantity,
    }

    textbox_inputs_given = {
        "notes": notes,
    }

    # Raise an error if mandatory fields are missing.
    for key, value in required_inputs.items():
        if value is None:
            raise ExceptionToUse(f"Missing {key} for transaction.")

    inputs_given_list = [
        (default_text_inputs_given, DEFAULT_TEXT_MAX_LENGTH),
        (unit_inputs_given, UNIT_INPUT_MAX_LENGTH),
        (textbox_inputs_given, TEXTBOX_MAX_LENGTH),
    ]

    # check length if the optional field was actually provided.
    for input_given, max_length in inputs_given_list:
        for key, value in input_given.items():
            if value and len(value) > max_length:
                raise ExceptionToUse(
                    f"Equipment {key} input must be less or equal to {max_length} characters."
                )

    return (
        item_type,
        item_id,
        item_name,
        transaction_type,
        quantity,
        date,
        notes,
    )


def get_edit_properties(request, ExceptionToUse: Exception):
    """
    Gets properties of transaction and validates the inputs.
    Delete and replace this function if edit form is the same as add form.
    """
    # Mandatory fields. (Currently none for edit.)
    # Optional fields.
    notes = request.POST.get("notes") or ""

    required_inputs = {}

    default_text_inputs_given = {}

    unit_inputs_given = {}

    textbox_inputs_given = {
        "notes": notes,
    }

    # Raise an error if mandatory fields are missing.
    for key, value in required_inputs.items():
        if value is None:
            raise ExceptionToUse(f"Missing {key} for transaction.")

    inputs_given_list = [
        (default_text_inputs_given, DEFAULT_TEXT_MAX_LENGTH),
        (unit_inputs_given, UNIT_INPUT_MAX_LENGTH),
        (textbox_inputs_given, TEXTBOX_MAX_LENGTH),
    ]

    # check length if the optional field was actually provided.
    for input_given, max_length in inputs_given_list:
        for key, value in input_given.items():
            if value and len(value) > max_length:
                raise ExceptionToUse(
                    f"Transaction {key} input must be less or equal to {max_length} characters."
                )

    return (notes,)


def search_filtering(form):
    transactions = Transaction.objects.all().order_by("-id")
    active_filters = []

    if form.is_valid():
        data = form.cleaned_data

        if data.get("id"):
            transactions = transactions.filter(id=data["id"])
            active_filters.append(f"ID: {str(data['id'])}")
        if data.get("item_type"):
            if data.get("item_type") != "None":
                transactions = transactions.filter(
                    item_type__icontains=data["item_type"]
                )
                active_filters.append(f"Item Type: {str(data['item_type'])}")
        if data.get("item_id"):
            transactions = transactions.filter(item_id=data["item_id"])
            active_filters.append(f"Item ID: {str(data['item_id'])}")
        if data.get("name"):
            transactions = transactions.filter(item_name__icontains=data["name"])
            active_filters.append(f"Item Name: {str(data['name'])}")
        if data.get("transaction_type"):
            if data.get("transaction_type") != "None":
                transactions = transactions.filter(
                    transaction_type__icontains=data["transaction_type"]
                )
                active_filters.append(
                    f"Transaction Type: {str(data['transaction_type'])}"
                )
        if data.get("qty_mode"):
            if data.get("qty_mode") != "all":
                if data.get("min_qty") is not None:
                    transactions = transactions.filter(quantity__gte=data["min_qty"])
                    active_filters.append(f"Min Quantity: {str(data['min_qty'])}")
                if data.get("max_qty") is not None:
                    transactions = transactions.filter(quantity__lte=data["max_qty"])
                    active_filters.append(f"Max Quantity: {str(data['max_qty'])}")
                if data.get("qty_mode") == "highest":
                    transactions = transactions.order_by("-quantity")
                    active_filters.append(f"Highest to Lowest Quantity")
                if data.get("qty_mode") == "lowest":
                    transactions = transactions.order_by("quantity")
                    active_filters.append(f"Lowest to Highest Quantity")
        if data.get("transaction_date_mode"):
            if data.get("transaction_date_mode") != "all":
                if data.get("min_transaction_date") is not None:
                    transactions = transactions.filter(
                        date__gte=data["min_transaction_date"]
                    )
                    active_filters.append(
                        f"Min Transaction Date: {str(data['min_transaction_date'])}"
                    )
                if data.get("max_transaction_date") is not None:
                    transactions = transactions.filter(
                        date__lte=data["max_transaction_date"]
                    )
                    active_filters.append(
                        f"Max Transaction Date: {str(data['max_transaction_date'])}"
                    )
                if data.get("transaction_date_mode") == "highest":
                    transactions = transactions.order_by("-date")
                    active_filters.append(f"Highest to Lowest Transaction Date")
                if data.get("transaction_date_mode") == "lowest":
                    transactions = transactions.order_by("date")
                    active_filters.append(f"Lowest to Highest Transaction Date")
    return active_filters, transactions


@login_required
def transaction_list(request, id=None):
    try:
        # FOR SEARCH FILTERING.
        form = TransactionSearchForm(request.GET)
        active_filters, transactions = search_filtering(form)

        # If ID was given in URL. Ex: transactions/id/<int>
        try:
            if (id):
                transactions = Transaction.objects.filter(id=id)

                if not transactions.exists():
                    raise Exception(f"Transaction of ID {id} does not exist.")
        except Exception as e:
            logger.log(f"Error in transactions view by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("transaction_list")

        # FOR PAGINATION.
        page_number = request.GET.get("page")
        page_obj, backward_pages, forward_pages, page_number = paginationFunction(
            transactions, page_number, 10
        )

        context = {
            "form": form,
            "search_filters_applied": active_filters,
            "list_url_given": "transaction_list",
            "add_url_given": "add_transaction",
            "edit_url_given": "edit_transaction",
            "delete_url_given": "delete_transaction",
            "page_obj": page_obj,
            "backward_pages": backward_pages,
            "forward_pages": forward_pages,
            "max_textbox_length": TEXTBOX_MAX_LENGTH,
            "max_input_text_length": DEFAULT_TEXT_MAX_LENGTH,
            "max_input_unit_length": UNIT_INPUT_MAX_LENGTH,
        }

        logger.log(f"User {request.user} viewed transaction list (page {page_number}).")
        return render(request, "app/transaction_list.html", context)
    except Exception as e:
        logger.log(f"Error in transactions view by {request.user}: {e}")
        messages.error(request, str(e))
        return redirect("error_page")


@login_required
def add_transaction(request):
    if request.method == "POST":
        try:
            (
                item_type,
                item_id,
                item_name,
                transaction_type,
                quantity,
                date,
                notes,
            ) = get_properties(request, TransactionCreationException)

            transaction = Transaction.objects.create(
                item_type=item_type,
                item_id=item_id,
                item_name=item_name,
                transaction_type=transaction_type,
                quantity=quantity,
                date=date,
                notes=notes,
            )
            logger.log(
                f"User {request.user} added transaction: {item_type} {item_id} (ID: {transaction.id})."
            )
            return redirect("transaction_list")
        except TransactionCreationException as e:
            logger.log(f"Transaction creation error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("transaction_list")
        except Exception as e:
            logger.log(
                f"Unexpected error during transaction creation by user {request.user}: {e}"
            )
            messages.error(
                request, "An unexpected error occurred while adding the transaction."
            )
            return redirect("transaction_list")
    return redirect("transaction_list")


@login_required
def edit_transaction(request):
    if request.method == "POST":
        try:
            try:
                transaction = get_object_or_404(Transaction, id=request.POST.get("id"))
            except Http404:
                raise TransactionEditException("Supply not found.")

            old_name = transaction.item_name

            (transaction.notes,) = get_edit_properties(
                request, TransactionEditException
            )

            transaction.save()

            name_change_msg = editStockNameChange(old_name, transaction.item_name)

            logger.log(
                f"User {request.user} edited transaction: {old_name} {name_change_msg} (ID: {transaction.id})."
            )
            return redirect("transaction_list")

        except TransactionEditException as e:
            logger.log(f"Transaction edit error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("transaction_list")
        except Exception as e:
            logger.log(f"Unexpected error during transaction edit: {e}")
            messages.error(
                request, "An unexpected error occurred while editing the transaction."
            )
            return redirect("transaction_list")
    return redirect("transaction_list")


@login_required
def delete_transaction(request):
    if request.method == "POST":
        try:
            try:
                transaction = get_object_or_404(Transaction, id=request.POST.get("id"))
            except Http404:
                raise TransactionDeleteException("Transaction not found.")

            transaction_item_type = transaction.item_type
            transaction_item_id = transaction.item_id
            transaction_id = transaction.id
            transaction.delete()

            logger.log(
                f"User {request.user} deleted transaction: {transaction_item_type} of ID {transaction_item_id} (ID: {transaction_id})."
            )
            return redirect("transaction_list")
        except TransactionDeleteException as e:
            logger.log(f"Transaction delete error by {request.user}: {e}")
            messages.error(request, str(e))
            return redirect("transaction_list")
        except Exception as e:
            logger.log(
                f"Unexpected error during transaction deletion by user {request.user}: {e}"
            )
            messages.error(
                request, "An unexpected error occured while deleting the transaction."
            )
            return redirect("transaction_list")
    return redirect("transaction_list")
