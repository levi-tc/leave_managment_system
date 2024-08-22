from django import forms
from .models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'other_leave_type', 'start_date', 'end_date', 'return_date', 'total_days', 'reason', 'contact_during_leave']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        leave_type = cleaned_data.get('leave_type')
        other_leave_type = cleaned_data.get('other_leave_type')

        if leave_type == 'other' and not other_leave_type:
            raise forms.ValidationError("Please specify the other leave type.")

        return cleaned_data