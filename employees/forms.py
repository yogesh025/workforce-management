from django import forms

class EmployeeUploadForm(forms.Form):
    csv_file = forms.FileField()
