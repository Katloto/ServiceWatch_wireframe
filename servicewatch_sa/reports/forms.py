# reports/forms.py
from django import forms
from .models import IssueReport

class IssueReportForm(forms.ModelForm):
    class Meta:
        model = IssueReport
        fields = ['category', 'description', 'photo', 'latitude', 'longitude', 
                  'address', 'reporter_name', 'reporter_email', 'reporter_phone']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the issue...'}),
            'address': forms.TextInput(attrs={'placeholder': 'Street address or landmark'}),
        }