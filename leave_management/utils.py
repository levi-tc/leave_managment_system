# leave_management/utils.py

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_leave_request_pdf(leave_request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['Normal']

    # Title
    elements.append(Paragraph("Leave Request Form", title_style))
    elements.append(Spacer(1, 12))

    # Leave Request Details
    data = [
        ["Employee Name:", leave_request.user.get_full_name()],
        ["Leave Type:", leave_request.get_leave_type_display()],
        ["Start Date:", leave_request.start_date.strftime("%Y-%m-%d")],
        ["End Date:", leave_request.end_date.strftime("%Y-%m-%d")],
        ["Return Date:", leave_request.return_date.strftime("%Y-%m-%d")],
        ["Total Days:", str(leave_request.total_days)],
        ["Reason:", leave_request.reason],
        ["Contact During Leave:", leave_request.contact_during_leave],
        ["Status:", leave_request.get_status_display()],
    ]

    if leave_request.leave_type == 'other':
        data.insert(2, ["Other Leave Type:", leave_request.other_leave_type])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    # Build PDF
    doc.build(elements)

    buffer.seek(0)
    return buffer