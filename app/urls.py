from django.urls import path

from .backend.crop.crop import add_crop, crop_list, delete_crop, edit_crop
from .backend.dashboard.dashboard import dashboard
from .backend.equipment.equipment import (add_equipment, delete_equipment,
                                          edit_equipment, equipment_list)
from .backend.livestock.livestock import (add_livestock, delete_livestock,
                                          edit_livestock, livestock_list)
from .backend.recent_activities.recent_activities import recent_activities_list, download_all_activities
from .backend.reports.reports import reports
from .backend.supplies.supplies import (add_supplies, delete_supplies,
                                        edit_supplies, supplies_list)
from .backend.transactions.transaction import (add_transaction,
                                               delete_transaction,
                                               transaction_list)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    # Livestock URLs
    path("livestock/", livestock_list, name="livestock_list"),
    path("livestock/add/", add_livestock, name="add_livestock"),
    path("livestock/edit/", edit_livestock, name="edit_livestock"),
    path("livestock/delete/", delete_livestock, name="delete_livestock"),
    # Crop URLs
    path("crops/", crop_list, name="crop_list"),
    path("crops/add/", add_crop, name="add_crop"),
    path("crops/edit/", edit_crop, name="edit_crop"),
    path("crops/delete/", delete_crop, name="delete_crop"),
    # Equipment URLs
    path("equipment/", equipment_list, name="equipment_list"),
    path("equipment/add/", add_equipment, name="add_equipment"),
    path("equipment/edit/", edit_equipment, name="edit_equipment"),
    path("equipment/delete/", delete_equipment, name="delete_equipment"),
    # Supplies URLs
    path("supplies/", supplies_list, name="supplies_list"),
    path("supplies/add/", add_supplies, name="add_supplies"),
    path("supplies/edit/", edit_supplies, name="edit_supplies"),
    path("supplies/delete/", delete_supplies, name="delete_supplies"),
    # Transaction URLs
    path("transactions/", transaction_list, name="transaction_list"),
    path("transactions/add/", add_transaction, name="add_transaction"),
    path("transactions/delete/", delete_transaction, name="delete_transaction"),
    # Reports URLs
    path("reports/", reports, name="reports"),
    # Recent activites URLs
    path("recent_activities/", recent_activities_list, name="recent_activities_list"),
    path("recent_activities/download_logs", download_all_activities, name="download_all_activities"),
]
