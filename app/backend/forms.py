from django import forms
from .models import Supplies

class SuppliesSearchForm(forms.Form):
    id = forms.IntegerField(required=False, label='Search by ID')
    name = forms.CharField(required=False, label='Search by Name')
    category = forms.CharField(required=False, label='Category')
    # quantity = forms.FloatField(required=False, label='Quantity')
    min_qty = forms.IntegerField(required=False, label="Min Quantity")
    max_qty = forms.IntegerField(required=False, label="Max Quantity")
    unit = forms.CharField(required=False, label='Unit')
    minimum_required = forms.FloatField(required=False, label='Minimum Required')
    cost_per_unit = forms.FloatField(required=False, label='Cost Per Unit ( $ )')
    last_restocked = forms.DateField(required=False, label='Last Restocked')
    procurement_date = forms.DateField(required=False, label='Procurement Date')