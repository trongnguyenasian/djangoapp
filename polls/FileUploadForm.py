from django import forms

class FileUploadForm(forms.Form):
    test = forms.FileField()
