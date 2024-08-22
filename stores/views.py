
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import StoreCreationForm

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

@user_passes_test(is_admin)
def create_store(request):
    if request.method == 'POST':
        form = StoreCreationForm(request.POST)
        if form.is_valid():
            store = form.save()
            messages.success(request, f'Store "{store.name}" has been created successfully.')
            return redirect('store_list')  # Make sure you have a 'store_list' URL or change this to an appropriate URL
    else:
        form = StoreCreationForm()
    
    return render(request, 'stores/create_store.html', {'form': form})