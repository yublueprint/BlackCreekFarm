from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

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
            name = request.POST.get("name")
            category = request.POST.get("category")
            transaction_type = request.POST.get("transaction_type")  
            amount = request.POST.get("amount")
            date = request.POST.get("date")
            notes = request.POST.get("notes", "")

            Transaction.objects.create(
                name=name,
                category=category,
                transaction_type=transaction_type,  
                amount=amount,
                date=date,
                notes=notes
            )
            logger.log(f"User {request.user} added a transaction.")
            return redirect("transaction_list")
        except Exception as e:
            logger.log(f"Error adding transaction by user {request.user}: {e}")
            return render(request, "app/transaction_list.html", {
                "transactions": Transaction.objects.all(),
                "error": "Failed to add transaction."
            })

@login_required
def edit_transaction(request):
    if request.method == "POST":
        try:
            txn = get_object_or_404(Transaction, id=request.POST.get("id"))
            txn.name = request.POST.get("name")
            txn.category = request.POST.get("category")
            txn.transaction_type = request.POST.get("transaction_type")  
            txn.amount = request.POST.get("amount")
            txn.date = request.POST.get("date")
            txn.notes = request.POST.get("notes", "")
            txn.save()
            logger.log(f"User {request.user} edited transaction {txn.id}.")
            return redirect("transaction_list")
        except Exception as e:
            logger.log(f"Error editing transaction by user {request.user}: {e}")
            return render(request, "app/transaction_list.html", {
                "transactions": Transaction.objects.all(),
                "error": "Failed to edit transaction."
            })

@login_required
def delete_transaction(request):
    if request.method == "POST":
        try:
            txn = get_object_or_404(Transaction, id=request.POST.get("id"))
            txn.delete()
            logger.log(f"User {request.user} deleted transaction {txn.id}.")
            return redirect("transaction_list")
        except Exception as e:
            logger.log(f"Error deleting transaction by user {request.user}: {e}")
            return render(request, "app/transaction_list.html", {
                "transactions": Transaction.objects.all(),
                "error": "Failed to delete transaction."
            })
