import csv
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from openpyxl import Workbook

# Reportlab imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from apps.employees.models import Employee
from apps.attendance.models import Attendance
from apps.leaves.models import LeaveRequest
from apps.payroll.models import Payroll
from apps.recruitment.models import Candidate


def is_hr_or_admin(user):
    return user.role in ('Super Admin', 'HR Manager')


@login_required
def report_dashboard(request):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")
        
    return render(request, 'reports/report_dashboard.html', {
        'months': Payroll.MONTH_CHOICES,
        'current_year': timezone.localdate().year
    })


@login_required
def report_payslip(request, pk):
    record = get_object_or_404(Payroll, pk=pk)
    
    # Check authorization (Employees can only download their own payslips)
    if request.user.role == 'Employee':
        profile = getattr(request.user, 'employee_profile', None)
        if not profile or record.employee != profile:
            return HttpResponseForbidden("Not authorized to download this payslip.")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{record.employee.employee_id}_{record.month}_{record.year}.pdf"'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#6366f1'),
        alignment=1,
        spaceAfter=20
    )
    
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.HexColor('#1e293b')
    )
    
    val_style = ParagraphStyle(
        'ValStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#475569')
    )

    story.append(Paragraph("HUMAN RESOURCE MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph(f"PAYSLIP FOR {record.get_month_display().upper()} {record.year}", ParagraphStyle('Sub', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, alignment=1, spaceAfter=20)))
    
    # Employee Info Table
    emp_data = [
        [Paragraph("Employee Name:", label_style), Paragraph(f"{record.employee.first_name} {record.employee.last_name}", val_style),
         Paragraph("Employee ID:", label_style), Paragraph(record.employee.employee_id, val_style)],
        [Paragraph("Designation:", label_style), Paragraph(record.employee.designation, val_style),
         Paragraph("Department:", label_style), Paragraph(record.employee.department.name if record.employee.department else "-", val_style)],
    ]
    t_emp = Table(emp_data, colWidths=[100, 160, 100, 160])
    t_emp.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_emp)
    story.append(Spacer(1, 20))
    
    # Salary details
    sal_structure = getattr(record.employee, 'salary_structure', None)
    basic = sal_structure.base_salary if sal_structure else 0
    hra = sal_structure.hra if sal_structure else 0
    allowances = sal_structure.allowances if sal_structure else 0
    fixed_deductions = sal_structure.deductions if sal_structure else 0
    
    sal_data = [
        [Paragraph("Earnings", label_style), Paragraph("Amount ($)", label_style),
         Paragraph("Deductions", label_style), Paragraph("Amount ($)", label_style)],
        [Paragraph("Base Salary", val_style), Paragraph(f"{basic:.2f}", val_style),
         Paragraph("Fixed Deductions", val_style), Paragraph(f"{fixed_deductions:.2f}", val_style)],
        [Paragraph("HRA", val_style), Paragraph(f"{hra:.2f}", val_style),
         Paragraph("Unpaid Leave Deductions", val_style), Paragraph(f"{(record.total_deductions - fixed_deductions):.2f}", val_style)],
        [Paragraph("Allowances", val_style), Paragraph(f"{allowances:.2f}", val_style),
         Paragraph("", val_style), Paragraph("", val_style)],
        [Paragraph("Gross Earnings", label_style), Paragraph(f"{record.gross_salary:.2f}", label_style),
         Paragraph("Total Deductions", label_style), Paragraph(f"{record.total_deductions:.2f}", label_style)]
    ]
    
    t_sal = Table(sal_data, colWidths=[130, 130, 130, 130])
    t_sal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#f8fafc')),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#cbd5e1')),
        ('LINEABOVE', (0,-1), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sal)
    story.append(Spacer(1, 20))
    
    # Net Pay Callout
    net_data = [
        [Paragraph("NET PAYABLE AMOUNT (ROUNDED)", label_style), Paragraph(f"${record.net_salary:.2f}", ParagraphStyle('NetAmt', parent=label_style, fontSize=14, textColor=colors.HexColor('#10b981')))]
    ]
    t_net = Table(net_data, colWidths=[300, 220])
    t_net.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ecfdf5')),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor('#a7f3d0')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_net)
    
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


@login_required
def export_report(request):
    if not is_hr_or_admin(request.user):
        return HttpResponseForbidden("Not authorized.")

    report_type = request.GET.get('type')
    format_type = request.GET.get('format', 'csv')
    
    # 1. Fetch Data
    headers = []
    rows = []
    title = f"{report_type} Report"

    if report_type == 'employees':
        headers = ['Employee ID', 'Name', 'Email', 'Phone', 'Role', 'Status', 'Department']
        data = Employee.objects.all().select_related('user', 'department')
        for emp in data:
            rows.append([emp.employee_id, f"{emp.first_name} {emp.last_name}", emp.personal_email or emp.user.email, emp.phone, emp.user.role, emp.employment_status, emp.department.name if emp.department else "-"])
            
    elif report_type == 'attendance':
        headers = ['Employee ID', 'Name', 'Date', 'Clock In', 'Clock Out', 'Status', 'Remarks']
        data = Attendance.objects.all().select_related('employee')
        for record in data:
            rows.append([record.employee.employee_id, f"{record.employee.first_name} {record.employee.last_name}", record.date, record.check_in, record.check_out, record.status, record.remarks])
            
    elif report_type == 'leaves':
        headers = ['Employee Name', 'Leave Type', 'Start Date', 'End Date', 'Reason', 'Status']
        data = LeaveRequest.objects.all().select_related('employee')
        for leave in data:
            rows.append([f"{leave.employee.first_name} {leave.employee.last_name}", leave.leave_type, leave.start_date, leave.end_date, leave.reason, leave.status])
            
    elif report_type == 'payroll':
        headers = ['Employee ID', 'Name', 'Period', 'Gross Salary', 'Deductions', 'Net Salary']
        data = Payroll.objects.all().select_related('employee')
        for pay in data:
            rows.append([pay.employee.employee_id, f"{pay.employee.first_name} {pay.employee.last_name}", f"{pay.get_month_display()} {pay.year}", pay.gross_salary, pay.total_deductions, pay.net_salary])
            
    elif report_type == 'recruitment':
        headers = ['Candidate', 'Email', 'Role Applied', 'Experience', 'Status']
        data = Candidate.objects.all().select_related('job_opening')
        for cand in data:
            rows.append([f"{cand.first_name} {cand.last_name}", cand.email, cand.job_opening.title if cand.job_opening else "General", cand.experience, cand.status])
            
    else:
        return redirect('report_dashboard')

    # 2. Formats
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.csv"'
        writer = csv.writer(response)
        writer.writerow(headers)
        writer.writerows(rows)
        return response
        
    elif format_type == 'excel':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = "Report"
        ws.append(headers)
        for row in rows:
            # Map items to string or numeric types to prevent Excel loading failures
            ws.append([str(item) if item is not None else "" for item in row])
        wb.save(response)
        return response
        
    elif format_type == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.pdf"'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'ReportTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#6366f1'), spaceAfter=15
        )
        hdr_style = ParagraphStyle(
            'RepHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#1e293b')
        )
        cell_style = ParagraphStyle(
            'RepCell', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor('#475569')
        )
        
        story.append(Paragraph(title.upper(), title_style))
        story.append(Spacer(1, 10))
        
        table_data = [[Paragraph(h, hdr_style) for h in headers]]
        for r in rows:
            table_data.append([Paragraph(str(item) if item is not None else "-", cell_style) for item in r])
            
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        
        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
        
    return redirect('report_dashboard')
