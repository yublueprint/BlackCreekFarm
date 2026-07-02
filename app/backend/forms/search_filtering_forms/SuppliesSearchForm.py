from django import forms

from app.backend.forms.search_filtering_forms.shared_variables import \
    search_dropdown_choices


class SuppliesSearchForm(forms.Form):
    id = forms.IntegerField(required=False, label="Search by ID")
    name = forms.CharField(required=False, label="Search by Name")
    category = forms.CharField(required=False, label="Category")
    qty_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Quantity Filter",
    )
    min_qty = forms.FloatField(required=False, label="Min Quantity")
    max_qty = forms.FloatField(required=False, label="Max Quantity")
    unit = forms.CharField(required=False, label="Unit")
    minimum_required = forms.FloatField(required=False, label="Minimum Required")
    cost_per_unit = forms.FloatField(required=False, label="Cost Per Unit ( $ )")
    last_restocked_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Last Restocked Filter",
    )
    min_last_restocked = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    max_last_restocked = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    procurement_date_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Procurement Date Filter",
    )
    min_procurement_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    max_procurement_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
