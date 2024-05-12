from  django import forms
from .models import Dataset, Certificate, Report

class UploadForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'accept': 'application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'})
        }   

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'
        exclude = ['user', 'hash', 'previous_hash', 'created_at']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'