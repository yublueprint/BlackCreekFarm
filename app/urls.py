from django.contrib.auth.decorators import login_required
from django.urls import path

from .backend.alerts.alerts import (alerts_list, mark_alert_read,
                                    mark_all_alerts_read)
from .backend.crop.crop import add_crop, crop_list, delete_crop, edit_crop
from .backend.dashboard.dashboard import dashboard
from .backend.equipment.equipment import (add_equipment, delete_equipment,
                                          edit_equipment, equipment_list)
from .backend.error_page.error_page import error_page
from .backend.livestock.livestock import (add_livestock, delete_livestock,
                                          edit_livestock, livestock_list)
from .backend.recent_activities.recent_activities import (
    download_all_activities, recent_activities_list)
from .backend.reports.reports import download_livestock_report, reports
from .backend.stock_backups.stock_backups import download_backup, stock_backups
from .backend.qr_scanner.qr_scanner import qr_scanner_page, qr_scanner_camera, manually_find_item
from .backend.supplies.supplies import (add_supplies, delete_supplies,
                                        edit_supplies, supplies_list)
from .backend.transactions.transaction import (add_transaction,
                                               delete_transaction,
                                               edit_transaction,
                                               transaction_list)

urlpatterns = [
    path("", login_required(dashboard), name="dashboard"),
    # Livestock URLs
    path("livestock/", livestock_list, name="livestock_list"),
    path("livestock/id/<int:id>/", livestock_list, name="load_livestock"),
    path("livestock/add/", add_livestock, name="add_livestock"),
    path("livestock/edit/", edit_livestock, name="edit_livestock"),
    path("livestock/delete/", delete_livestock, name="delete_livestock"),
    # Crop URLs
    path("crops/", crop_list, name="crop_list"),
    path("crops/id/<int:id>/", crop_list, name="load_crop"),
    path("crops/add/", add_crop, name="add_crop"),
    path("crops/edit/", edit_crop, name="edit_crop"),
    path("crops/delete/", delete_crop, name="delete_crop"),
    # Equipment URLs
    path("equipment/", equipment_list, name="equipment_list"),
    path("equipment/id/<int:id>/", equipment_list, name="load_equipment"),
    path("equipment/add/", add_equipment, name="add_equipment"),
    path("equipment/edit/", edit_equipment, name="edit_equipment"),
    path("equipment/delete/", delete_equipment, name="delete_equipment"),
    # Supplies URLs
    path("supplies/", supplies_list, name="supplies_list"),
    path("supplies/id/<int:id>/", supplies_list, name="load_supply"),
    path("supplies/add/", add_supplies, name="add_supplies"),
    path("supplies/edit/", edit_supplies, name="edit_supplies"),
    path("supplies/delete/", delete_supplies, name="delete_supplies"),
    # Transaction URLs
    path("transactions/", transaction_list, name="transaction_list"),
    path("transactions/id/<int:id>/", transaction_list, name="load_transaction"),
    path("transactions/add/", add_transaction, name="add_transaction"),
    path("transactions/edit/", edit_transaction, name="edit_transaction"),
    path("transactions/delete/", delete_transaction, name="delete_transaction"),
    # Reports URLs
    path("reports/", reports, name="reports"),
    path(
        "reports/livestock/pdf/",
        download_livestock_report,
        name="download_livestock_report",
    ),
    # Stock Backups URLs
    path("stock_backups/", stock_backups, name="stock_backups"),
    path("stock_backups/download", download_backup, name="download_backup"),
    # QR Scanner URLs
    path("qr_scanner/", qr_scanner_page, name="qr_scanner_page"),
    path("qr_scanner/camera_scan", qr_scanner_camera, name="qr_scanner_camera"),
    path("qr_scanner/find_item/", manually_find_item, name="manually_find_item"),
    # Alert URLs
    path("alerts/", alerts_list, name="alerts_list"),
    path("alerts/red/<int:alert_id>/", mark_alert_read, name="mark_alert_read"),
    path("alerts/mark_all_read/", mark_all_alerts_read, name="mark_all_alerts_read"),
    # Recent activites URLs
    path("recent_activities/", recent_activities_list, name="recent_activities_list"),
    path(
        "recent_activities/download_logs",
        download_all_activities,
        name="download_all_activities",
    ),
    # Error Page
    path("errors/", error_page, name="error_page"),
]
