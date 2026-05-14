from django import forms


class SuppliesSearchForm(forms.Form):
    id = forms.IntegerField(required=False, label="Search by ID")
    name = forms.CharField(required=False, label="Search by Name")
    category = forms.CharField(required=False, label="Category")
    # quantity = forms.FloatField(required=False, label='Quantity')
    qty_mode = forms.ChoiceField(
        choices=[("all", "Any Quantity"), ("range", "Specific Range")],
        required=False,
        label="Quantity Filter",
    )
    min_qty = forms.FloatField(required=False, label="Min Quantity")
    max_qty = forms.FloatField(required=False, label="Max Quantity")
    unit = forms.CharField(required=False, label="Unit")
    minimum_required = forms.FloatField(required=False, label="Minimum Required")
    cost_per_unit = forms.FloatField(required=False, label="Cost Per Unit ( $ )")
    last_restocked_mode = forms.ChoiceField(
        choices=[("all", "Any Date"), ("range", "Specific Range")],
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
        choices=[("all", "Any Date"), ("range", "Specific Range")],
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


class LivestockSearchForm(forms.Form):
    # ID
    id = forms.IntegerField(required=False, label="Search by ID")
    # NAME
    name = forms.CharField(required=False, label="Search by Name")
    # TYPE
    type = forms.CharField(required=False, label="Type")
    # AGE
    age_mode = forms.ChoiceField(
        choices=[("all", "Any Age"), ("range", "Specific Range")],
        required=False,
        label="Age Filter",
    )
    min_age = forms.IntegerField(required=False, label="Min Age")
    max_age = forms.IntegerField(required=False, label="Max Age")
    # WEIGHT
    weight_mode = forms.ChoiceField(
        choices=[("all", "Any Weight"), ("range", "Specific Range")],
        required=False,
        label="Weight Filter",
    )
    min_weight = forms.FloatField(required=False, label="Min Weight")
    max_weight = forms.FloatField(required=False, label="Max Weight")
    # HEALTH STATUS
    health_status = forms.CharField(required=False, label="Health Status")
    # PURCHASE PRICE
    purchase_price_mode = forms.ChoiceField(
        choices=[("all", "Any Price"), ("range", "Specific Range")],
        required=False,
        label="Purchase Price Filter",
    )
    min_purchase_price = forms.FloatField(required=False, label="Min Purchase Price")
    max_purchase_price = forms.FloatField(required=False, label="Max Purchase Price")
    # CURRENT VALUE
    current_value_mode = forms.ChoiceField(
        choices=[("all", "Any Price"), ("range", "Specific Range")],
        required=False,
        label="Current Value Filter",
    )
    min_current_value = forms.FloatField(required=False, label="Min Current Value")
    max_current_value = forms.FloatField(required=False, label="Max Current Value")
    # NEXT VACCINATION DATE
    next_vaccination_mode = forms.ChoiceField(
        choices=[("all", "Any Date"), ("range", "Specific Range")],
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
