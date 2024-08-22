# leave_management/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import LeaveRequest
from .forms import LeaveRequestForm
from .utils import generate_leave_request_pdf

@login_required
def leave_request_list(request):
    leave_requests = LeaveRequest.objects.filter(user=request.user)
    return render(request, 'leave_management/leave_request_list.html', {'leave_requests': leave_requests})

@login_required
def create_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = request.user
            leave_request.store = request.user.store  # Assuming user has a store attribute
            leave_request.save()
            
            # Generate PDF
            pdf = generate_leave_request_pdf(leave_request)
            
            # Create HTTP response with PDF
            response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="leave_request_{leave_request.id}.pdf"'
            
            messages.success(request, 'Leave request submitted successfully. PDF generated and downloaded.')
            return response
    else:
        form = LeaveRequestForm()
    return render(request, 'leave_management/create_leave_request.html', {'form': form})

@login_required
def leave_request_detail(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk, user=request.user)
    return render(request, 'leave_management/leave_request_detail.html', {'leave_request': leave_request})

@login_required
def download_leave_request_pdf(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk, user=request.user)
    pdf = generate_leave_request_pdf(leave_request)
    
    response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="leave_request_{leave_request.id}.pdf"'
    return response