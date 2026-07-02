from django import forms

from app.backend.forms.search_filtering_forms.shared_variables import \
    search_dropdown_choices


class CropSearchForm(forms.Form):
    id = forms.IntegerField(required=False, label="Search by ID")
    name = forms.CharField(required=False, label="Search by Name")
    crop_type = forms.CharField(required=False, label="Search by Type")
    planting_date_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Planting Date Filter",
    )
    min_planting_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    max_planting_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    harvest_date_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Harvest Date Filter",
    )
    min_harvest_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    max_harvest_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    expected_yield_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Expected Yield Filter",
    )
    min_expected_yield = forms.FloatField(required=False, label="Min Expected Yield")
    max_expected_yield = forms.FloatField(required=False, label="Max Expected Yield")
    yield_efficiency_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Yield Efficiency Filter",
    )
    min_yield_efficiency = forms.FloatField(
        required=False, label="Min Yield Efficiency"
    )
    max_yield_efficiency = forms.FloatField(
        required=False, label="Max Yield Efficiency"
    )
    water_usage_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Water Usage Filter",
    )
    min_water_usage = forms.FloatField(required=False, label="Min Water Usage")
    max_water_usage = forms.FloatField(required=False, label="Max Water Usage")
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
    region = forms.CharField(required=False, label="Search by Region")
