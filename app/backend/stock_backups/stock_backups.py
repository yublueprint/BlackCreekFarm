import csv
import io
import zipfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect, render

from app.logging.logging import Logger

from ..models import (Livestock, Crop, Equipment, Supplies, Transaction)

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

logger = Logger("app/logging/app.log")

@login_required
def stock_backups(request):
    try:
        context = {

        }

        logger.log(f"User {request.user} viewed stock backups page.")
        return render(request, "app/stock_backups.html", context)
    except Exception as e:
        logger.log(f"Error in stock backups view by {request.user}: {e}")
        messages.error(request, str(e))
        return redirect("error_page")

@login_required
def download_backup(request):
    try:
        stock_chosen = request.POST.get("stock_selector")

        valid_options = ["Livestock", "Crop", "Equipment", "Supplies", "Transactions"]

        model = None
        headers_given = []
        properties_given = []

        if stock_chosen in valid_options:
            if stock_chosen == "Livestock":
                model = Livestock
                headers_given = ['ID', 'Name', 'Type/Species', 'Age', 'Weight (kg)', 'Health', 'Purchase Price', 'Value ($)', 'Next Vaccination', 'Notes']
                properties_given = ['id', 'name', 'type', 'age', 'weight', 'health_status', 'purchase_price', 'current_value', 'next_vaccination_date', 'notes']
            elif stock_chosen == "Crop":
                model = Crop
                headers_given = ['ID', 'Name', 'Crop Type', 'Planting Date', 'Harvest Date', 'Expected Yield', 'Yield Efficiency', 'Water Usage', 'Next Checkup', 'Region', 'Notes']
                properties_given = ['id', 'name', 'crop_type', 'planting_date', 'harvest_date', 'expected_yield', 'yield_efficiency', 'water_usage_liters', 'next_checkup', 'region', 'notes']
            elif stock_chosen == "Equipment":
                model = Equipment
                headers_given = ['ID', 'Name', 'Category', 'Type', 'Serial Number', 'Purchase Date', 'Maintenance Due', 'Next Checkup', 'Warranty Expiry', 'Location', 'Supplier', 'Hours Used', 'Condition', 'Purchase Cost', 'Active', 'Last Service By', 'Service Interval Days', 'Maintenance History', 'Notes']
                properties_given = ['id', 'name', 'category', 'type', 'serial_number', 'purchase_date', 'maintenance_due', 'next_checkup', 'warranty_expiry', 'location', 'supplier', 'hours_used', 'condition', 'purchase_cost', 'active', 'last_service_by', 'service_interval_days', 'maintenance_history', 'notes']
            elif stock_chosen == "Supplies":
                model = Supplies
                headers_given = ['ID', 'Name', 'Category', 'Quantity', 'Unit', 'Last Restocked', 'Minimum Required', 'Cost Per Unit ($)', 'Procurement Date', 'Notes']
                properties_given = ['id', 'name', 'category', 'quantity', 'unit', 'last_restocked', 'minimum_required', 'cost_per_unit', 'procurement_date', 'notes']
            elif stock_chosen == "Transactions":
                model = Transaction
                headers_given = ['ID', 'Item Type', 'Item ID', 'Item Name', 'Type', 'Quantity', 'Date', 'Notes']
                properties_given = ['id', 'item_type', 'item_id', 'item_name', 'transaction_type', 'quantity', 'date', 'notes']
        else:
            raise Exception(f"{stock_chosen} is not a valid option.")
    
        queryset = model.objects.all().order_by("-id")

        # Creating ZIP file to contain both CSV and PDF.
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Creating the CSV in memory.
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(headers_given)

            rows = []
            for obj in queryset:
                row_data = [getattr(obj, property) for property in properties_given]
                writer.writerow(row_data)
                rows.append(row_data)
            
            zip_file.writestr(f"{stock_chosen}_List.csv", csv_buffer.getvalue())

            # Creating the PDF in memory.
            pdf_buffer = io.BytesIO()
        
            doc = SimpleDocTemplate(
                pdf_buffer, 
                pagesize=landscape(letter),
                rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
            )
            
            story = []
            styles = getSampleStyleSheet()
            
            cell_style = ParagraphStyle(
                'CellText',
                parent=styles['Normal'],
                fontSize=9,
                leading=11
            )
            header_style = ParagraphStyle(
                'HeaderText',
                parent=styles['Normal'],
                fontSize=10,
                leading=12,
                fontName='Helvetica-Bold',
                textColor=colors.whitesmoke
            )

            story.append(Paragraph(f"<b>{stock_chosen}</b>", styles['Title']))
            story.append(Spacer(1, 15))

            table_data = [[Paragraph(h, header_style) for h in headers_given]]
            for row in rows:
                table_data.append([Paragraph(str(item) if item is not None else "", cell_style) for item in row])

            pdf_table = Table(table_data, colWidths=None, hAlign='LEFT')
            
            pdf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')), # Dark header background
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]) # Zebra stripes
            ]))
            
            story.append(pdf_table)
            
            doc.build(story)
            
            zip_file.writestr(f"{stock_chosen}_List.pdf", pdf_buffer.getvalue())

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{stock_chosen}_Backup.zip"'

        return response
    except Exception as e:
        logger.log(f"Error while downloading backup of {stock_chosen} by {request.user}: {e}")
        messages.error(request, str(e))
        return redirect("stock_backups")