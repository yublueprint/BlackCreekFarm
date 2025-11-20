from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from app.logging.logging import Logger

from ..models import Transaction

logger = Logger("app/logging/app.log")


@login_required
def transaction_list(request):
    logger.log(f"User {request.user} viewed transaction list.")
    transactions = Transaction.objects.all()
    return render(request, "app/transaction_list.html", {"transactions": transactions})


@login_required
def add_transaction(request):
    if request.method == "POST":
        try:
            item_type = request.POST.get("item_type")
            item_id = request.POST.get("item_id")
            transaction_type = request.POST.get("transaction_type")
            quantity = request.POST.get("quantity")
            date = request.POST.get("date")

            Transaction.objects.create(
                item_type=item_type,
                item_id=item_id,
                transaction_type=transaction_type,
                quantity=quantity,
                date=date,
            )
            logger.log(f"User {request.user} added a transaction.")
            return redirect("transaction_list")
        except Exception as e:
            logger.log(f"Error adding transaction by user {request.user}: {e}")
            return render(
                request,
                "app/transaction_list.html",
                {
                    "transactions": Transaction.objects.all(),
                    "error": "Failed to add transaction.",
                },
            )


@login_required
def delete_transaction(request):
    if request.method == "POST":
        try:
            transaction = get_object_or_404(Transaction, id=request.POST.get("id"))
            transaction.delete()
            logger.log(f"User {request.user} deleted transaction.")
            return redirect("transaction_list")
        except Exception as e:
            logger.log(f"Error deleting transaction by user {request.user}: {e}")
            return render(
                request,
                "app/transaction_list.html",
                {
                    "transactions": Transaction.objects.all(),
                    "error": "Failed to delete transaction.",
                },
            )
