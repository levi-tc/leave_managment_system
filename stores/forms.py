from django import forms
from .models import Store

class StoreCreationForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'