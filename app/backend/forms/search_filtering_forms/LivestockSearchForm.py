from django import forms

from app.backend.forms.search_filtering_forms.shared_variables import \
    search_dropdown_choices


class LivestockSearchForm(forms.Form):
    # ID
    id = forms.IntegerField(required=False, label="Search by ID")
    # NAME
    name = forms.CharField(required=False, label="Search by Name")
    # TYPE
    type = forms.CharField(required=False, label="Type")
    # AGE
    age_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Age Filter",
    )
    min_age = forms.IntegerField(required=False, label="Min Age")
    max_age = forms.IntegerField(required=False, label="Max Age")
    # WEIGHT
    weight_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Weight Filter",
    )
    min_weight = forms.FloatField(required=False, label="Min Weight")
    max_weight = forms.FloatField(required=False, label="Max Weight")
    # HEALTH STATUS
    health_status = forms.CharField(required=False, label="Health Status")
    # PURCHASE PRICE
    purchase_price_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Purchase Price Filter",
    )
    min_purchase_price = forms.FloatField(required=False, label="Min Purchase Price")
    max_purchase_price = forms.FloatField(required=False, label="Max Purchase Price")
    # CURRENT VALUE
    current_value_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Current Value Filter",
    )
    min_current_value = forms.FloatField(required=False, label="Min Current Value")
    max_current_value = forms.FloatField(required=False, label="Max Current Value")
    # NEXT VACCINATION DATE
    next_vaccination_mode = forms.ChoiceField(
        choices=search_dropdown_choices,
        required=False,
        label="Next Vaccination Date Filter",
    )
    min_next_vaccination = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
    max_next_vaccination = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "data"},
            format="%Y-%m-%d",
        ),
    )
