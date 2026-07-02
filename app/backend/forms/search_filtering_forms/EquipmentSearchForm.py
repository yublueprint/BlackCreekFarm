from django import forms

from app.backend.forms.search_filtering_forms.shared_variables import \
    search_dropdown_choices


class EquipmentSearchForm(forms.Form):
    id = forms.IntegerField(required=False, label="Search by ID")
    name = forms.CharField(required=False, label="Search by Name")
    category = forms.CharField(required=False, label="Search by Category")
    type = forms.CharField(required=False, label="Search by Type")
    serial_number = forms.CharField(required=False, label="Search by Serial Number")
    purchase_date_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Purchase Date Filter",
    )
    min_purchase_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    max_purchase_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    maintenance_date_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Maintenance Date Filter",
    )
    min_maintenance_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    max_maintenance_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    next_checkup_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Next Checkup Date Filter",
    )
    min_next_checkup = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    max_next_checkup = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    warranty_expiration_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Warranty Expiration Filter",
    )
    min_warranty_expiration = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    max_warranty_expiration = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    location = forms.CharField(required=False, label="Search by Location")
    supplier = forms.CharField(required=False, label="Search by Supplier")
    hours_used_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Hours Used Filter",
    )
    min_hours_used = forms.FloatField(required=False, label="Min Hours Used")
    max_hours_used = forms.FloatField(required=False, label="Max Hours Used")
    condition = forms.CharField(required=False, label="Search by Condition")
    purchase_cost_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Purchase Cost Filter",
    )
    min_purchase_cost = forms.FloatField(required=False, label="Min Purchase Cost")
    max_purchase_cost = forms.FloatField(required=False, label="Max Purchase Cost")
    active = forms.CharField(required=False, label="Actively In Use")
    last_service_by = forms.CharField(required=False, label="Search by Last Service")
    service_interval_days_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Service Interval Days Filter",
    )
    min_service_interval_days = forms.FloatField(
        required=False, label="Min Service Interval Days"
    )
    max_service_interval_days = forms.FloatField(
        required=False, label="Max Service Interval Days"
    )
