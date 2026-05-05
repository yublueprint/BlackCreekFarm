from django.db import models

# Max text length for a Char field.
TEXTBOX_MAX_LENGTH = 2000
DEFAULT_TEXT_MAX_LENGTH = 100
UNIT_INPUT_MAX_LENGTH = 20


class Record(models.Model):
    name = models.CharField(max_length=DEFAULT_TEXT_MAX_LENGTH)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Livestock(models.Model):
    name = models.CharField(max_length=DEFAULT_TEXT_MAX_LENGTH)
    type = models.CharField(max_length=DEFAULT_TEXT_MAX_LENGTH)
    age = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    health_status = models.CharField(max_length=50, blank=True, null=True)
    purchase_price = models.FloatField(default=0, blank=True, null=True)
    current_value = models.FloatField(default=0, blank=True, null=True)
    next_vaccination_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.type}"


class Crop(models.Model):
    name = models.CharField(max_length=DEFAULT_TEXT_MAX_LENGTH)
    crop_type = models.CharField(max_length=DEFAULT_TEXT_MAX_LENGTH, default="unknown")
    planting_date = models.DateField()
    harvest_date = models.DateField(blank=True, null=True)
    expected_yield = models.FloatField(default=0)
    yield_efficiency = models.FloatField(default=0)
    water_usage_liters = models.FloatField(default=0)
    next_checkup = models.DateField(blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=DEFAULT_TEXT_MAX_LENGTH)
    category = models.CharField(max_length=50, default="N/A")
    type = models.CharField(max_length=DEFAULT_TEXT_MAX_LENGTH)
    purchase_date = models.DateField()
    maintenance_due = models.DateField()
    hours_used = models.FloatField(default=0)
    condition = models.CharField(max_length=50, default="Good")
    next_checkup = models.DateField(blank=True, null=True)
    purchase_cost = models.FloatField(default=0)
    notes = models.TextField(blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    warranty_expiry = models.DateField(blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True, null=True)
    maintenance_history = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    last_service_by = models.CharField(max_length=100, blank=True, null=True)
    service_interval_days = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Supplies(models.Model):
    name = models.CharField(max_length=DEFAULT_TEXT_MAX_LENGTH)
    category = models.CharField(max_length=DEFAULT_TEXT_MAX_LENGTH)
    quantity = models.FloatField()
    unit = models.CharField(max_length=UNIT_INPUT_MAX_LENGTH, blank=True, null=True)
    last_restocked = models.DateField(blank=True, null=True)
    minimum_required = models.FloatField(blank=True, null=True)
    cost_per_unit = models.FloatField(blank=True, null=True)
    procurement_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True, max_length=TEXTBOX_MAX_LENGTH)

    def __str__(self):
        return f"{self.name} ({self.category})"


class Transaction(models.Model):
    ITEM_TYPE_CHOICES = [
        ("Crop", "Crop"),
        ("Livestock", "Livestock"),
        ("Equipment", "Equipment"),
        ("Supplies", "Supplies"),
    ]

    TRANSACTION_TYPE_CHOICES = [
        ("Sale", "Sale"),
        ("Purchase", "Purchase"),
        ("Return", "Return"),
    ]

    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    item_id = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.transaction_type} of {self.item_type} (ID: {self.item_id})"
