
# Create your views here.
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.form import CustomUserCreationForm
from .models import CustomUser
from django.contrib import messages
from leave_management.models import LeaveRequest
from stores.models import Store
from django.views.decorators.http import require_http_methods

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

def is_store_manager(user):
    return user.is_authenticated and user.user_type == 'store_manager'

@login_required
@user_passes_test(lambda u: is_admin(u) or is_store_manager(u))
def register(request):
    if request.method == 'POST':
        user_type = 'employee' if is_store_manager(request.user) else request.POST.get('user_type')
        form = CustomUserCreationForm(request.POST, user_type=user_type)
        if form.is_valid():
            user = form.save(commit=False)
            if is_store_manager(request.user):
                user.store = request.user.store
            user.save()
            return redirect('user_list')  # Redirect to a user list view
    else:
        user_type = 'employee' if is_store_manager(request.user) else None
        form = CustomUserCreationForm(user_type=user_type)
    
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
def home(request):
    if request.user.user_type == 'admin':
        return redirect('user_list')
    elif request.user.user_type == 'store_manager':
        return redirect('store_dashboard')
    else:
        return redirect('employee_dashboard')

def is_store_manager(user):
    return user.is_authenticated and user.user_type == 'store_manager'

def is_employee(user):
    return user.is_authenticated and user.user_type == 'employee'

@login_required
def dashboard(request):
    user = request.user
    if user.user_type == 'admin':
        return admin_dashboard(request)
    elif user.user_type == 'store_manager':
        return store_dashboard(request)
    else:
        return employee_dashboard(request)

@login_required
@user_passes_test(is_store_manager)
def store_dashboard(request):
    store = request.user.store
    employees = CustomUser.objects.filter(store=store)
    leave_requests = LeaveRequest.objects.filter(store=store, status='pending')
    
    context = {
        'store': store,
        'employees': employees,
        'leave_requests': leave_requests,
    }
    return render(request, 'accounts/store_dashboard.html', context)

@login_required
@user_passes_test(is_employee)
def employee_dashboard(request):
    leave_requests = LeaveRequest.objects.filter(user=request.user)
    context = {
        'leave_requests': leave_requests,
    }
    return render(request, 'accounts/employee_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.user_type == 'admin')
def admin_dashboard(request):
    total_users = CustomUser.objects.count()
    total_stores = Store.objects.count()
    pending_leave_requests = LeaveRequest.objects.filter(status='pending').count()
    
    context = {
        'total_users': total_users,
        'total_stores': total_stores,
        'pending_leave_requests': pending_leave_requests,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@require_http_methods(["GET", "POST"])
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')