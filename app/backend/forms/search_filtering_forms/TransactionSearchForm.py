from django import forms

from app.backend.forms.search_filtering_forms.shared_variables import \
    search_dropdown_choices


class TransactionSearchForm(forms.Form):
    id = forms.IntegerField(required=False, label="Search by ID")
    item_type = forms.CharField(required=False, label="Search by Item Type")
    item_id = forms.IntegerField(required=False, label="Search by Item ID")
    name = forms.CharField(required=False, label="Search by Item Name")
    transaction_type = forms.CharField(
        required=False, label="Search by Transaction Type"
    )
    qty_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Quantity Filter",
    )
    min_qty = forms.FloatField(required=False, label="Min Quantity")
    max_qty = forms.FloatField(required=False, label="Max Quantity")
    transaction_date_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Transaction Date Filter",
    )
    min_transaction_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    max_transaction_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
