from django import forms

search_dropdown_choices = [("all", "Any"), ("range", "Specific Range"),
                           ("highest", "Highest to Lowest"), ("lowest", "Lowest to Highest")]


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
