from django.db import models

# NOTE: If trying to lower number while an object in the DB has higher number, it will cause error.
TEXTBOX_MAX_LENGTH = 2000
DEFAULT_TEXT_MAX_LENGTH = 100
UNIT_INPUT_MAX_LENGTH = 18 # Do not have it set to more than 18 as BigInt max limit is 18 digits.
DEFAULT_FILLER_TEXT = "N/A"


class Record(models.Model):
    name = models.CharField(max_length=DEFAULT_TEXT_MAX_LENGTH)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Livestock(models.Model):
    name = models.CharField(default=DEFAULT_FILLER_TEXT, max_length=DEFAULT_TEXT_MAX_LENGTH)
    type = models.CharField(default=DEFAULT_FILLER_TEXT, max_length=DEFAULT_TEXT_MAX_LENGTH)
    age = models.BigIntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    health_status = models.CharField(default=DEFAULT_FILLER_TEXT, blank=True, null=True, max_length=DEFAULT_TEXT_MAX_LENGTH)
    purchase_price = models.FloatField(default=0, blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    current_value = models.FloatField(default=0, blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    next_vaccination_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True, max_length=TEXTBOX_MAX_LENGTH)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Crop(models.Model):
    name = models.CharField(default=DEFAULT_FILLER_TEXT, max_length=DEFAULT_TEXT_MAX_LENGTH)
    crop_type = models.CharField(default=DEFAULT_FILLER_TEXT, max_length=DEFAULT_TEXT_MAX_LENGTH)
    planting_date = models.DateField(blank=True, null=True)
    harvest_date = models.DateField(blank=True, null=True)
    expected_yield = models.FloatField(default=0, blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    yield_efficiency = models.FloatField(default=0, blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    water_usage_liters = models.FloatField(default=0, blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    next_checkup = models.DateField(blank=True, null=True)
    region = models.CharField(default=DEFAULT_FILLER_TEXT, blank=True, null=True, max_length=DEFAULT_TEXT_MAX_LENGTH)
    notes = models.TextField(blank=True, null=True, max_length=TEXTBOX_MAX_LENGTH)

    def __str__(self):
        return f"{self.name} ({self.crop_type})"


class Equipment(models.Model):
    class activeChoices(models.TextChoices):
        YES = 'Yes', 'Yes'
        NO = 'No', 'No'

    name = models.CharField(default=DEFAULT_FILLER_TEXT, max_length=DEFAULT_TEXT_MAX_LENGTH)
    category = models.CharField(default=DEFAULT_FILLER_TEXT, max_length=DEFAULT_TEXT_MAX_LENGTH)
    type = models.CharField(default=DEFAULT_FILLER_TEXT, blank=True, null=True, max_length=DEFAULT_TEXT_MAX_LENGTH)
    serial_number = models.CharField(default=DEFAULT_FILLER_TEXT, blank=True, null=True, max_length=DEFAULT_TEXT_MAX_LENGTH)
    purchase_date = models.DateField(blank=True, null=True)
    maintenance_due = models.DateField(blank=True, null=True)
    next_checkup = models.DateField(blank=True, null=True)
    warranty_expiry = models.DateField(blank=True, null=True)
    location = models.CharField(default=DEFAULT_FILLER_TEXT, blank=True, null=True, max_length=DEFAULT_TEXT_MAX_LENGTH)
    supplier = models.CharField(default=DEFAULT_FILLER_TEXT, blank=True, null=True, max_length=DEFAULT_TEXT_MAX_LENGTH)
    hours_used = models.FloatField(default=0, blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    condition = models.CharField(default=DEFAULT_FILLER_TEXT, blank=True, null=True, max_length=DEFAULT_TEXT_MAX_LENGTH)
    purchase_cost = models.FloatField(default=0, blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    active = models.CharField(default=activeChoices.YES, choices=activeChoices, blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    last_service_by = models.CharField(default=DEFAULT_FILLER_TEXT, blank=True, null=True, max_length=DEFAULT_TEXT_MAX_LENGTH)
    service_interval_days = models.BigIntegerField(default=0, blank=True, null=True)
    maintenance_history = models.TextField(blank=True, null=True, max_length=DEFAULT_TEXT_MAX_LENGTH)
    notes = models.TextField(default="", blank=True, null=True, max_length=DEFAULT_TEXT_MAX_LENGTH)

    def __str__(self):
        return f"{self.name} ({self.category})"


class Supplies(models.Model):
    name = models.CharField(default=DEFAULT_FILLER_TEXT, max_length=DEFAULT_TEXT_MAX_LENGTH)
    category = models.CharField(default=DEFAULT_FILLER_TEXT, max_length=DEFAULT_TEXT_MAX_LENGTH)
    quantity = models.FloatField(max_length=UNIT_INPUT_MAX_LENGTH)
    unit = models.CharField(default=DEFAULT_FILLER_TEXT, blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    minimum_required = models.FloatField(blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    cost_per_unit = models.FloatField(blank=True, null=True, max_length=UNIT_INPUT_MAX_LENGTH)
    last_restocked = models.DateField(blank=True, null=True)
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

    item_type = models.CharField(choices=ITEM_TYPE_CHOICES, max_length=DEFAULT_TEXT_MAX_LENGTH)
    item_id = models.PositiveIntegerField()
    item_name = models.CharField(default=DEFAULT_FILLER_TEXT, max_length=DEFAULT_TEXT_MAX_LENGTH)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length=DEFAULT_TEXT_MAX_LENGTH)
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    notes = models.TextField(blank=True, null=True, max_length=TEXTBOX_MAX_LENGTH)

    def __str__(self):
        return f"{self.transaction_type} of {self.item_type} (ID: {self.item_id})"


class Alert(models.Model):
    SEVERITY_CHOICES = [
        ("INFO", "Info"),
        ("WARNING", "Warning"),
        ("CRITICAL", "Critical"),
    ]

    title = models.CharField(max_length=DEFAULT_TEXT_MAX_LENGTH)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default="INFO")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    item_type = models.CharField(max_length=50, blank=True, null=True)
    item_id = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"[{self.severity}] {self.title}"
