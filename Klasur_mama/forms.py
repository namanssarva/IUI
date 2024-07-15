from django import forms
from .models import UploadedDocument, PDFUpload

class DocumentForm(forms.ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ('file',)

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFUpload
        fields = ('pdf',)
