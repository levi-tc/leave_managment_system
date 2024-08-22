from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from stores.models import Store

CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    store = forms.ModelChoiceField(queryset=Store.objects.all(), required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('user_type', 'store')

    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super().__init__(*args, **kwargs)
        if user_type:
            self.fields['user_type'].initial = user_type
            self.fields['user_type'].widget = forms.HiddenInput()

        if user_type == 'employee':
            self.fields['store'].required = True
        elif user_type == 'store_manager':
            del self.fields['store']
        elif user_type == 'admin':
            del self.fields['store']

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.is_superuser:
            user.user_type = 'admin'
        if commit:
            user.save()
            if user.user_type == 'employee' and self.cleaned_data.get('store'):
                store = self.cleaned_data['store']
                store.employees.add(user)
        return user

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        store = cleaned_data.get('store')

        if user_type == 'employee' and not store:
            self.add_error('store', 'Store is required for employees.')
        elif user_type == 'store_manager' and store:
            self.add_error('store', 'Store should not be selected for store managers.')

        return cleaned_data