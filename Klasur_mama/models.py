from django.db import models
from django.contrib.auth.models import User

class UploadedDocument(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PDFUpload(models.Model):
    pdf = models.FileField(upload_to='pdfs/')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    pdf = models.ForeignKey(PDFUpload, on_delete=models.CASCADE)
    question_text = models.TextField()

class Summary(models.Model):
    pdf = models.ForeignKey(PDFUpload, on_delete=models.CASCADE)
    summary_text = models.TextField()

class Flashcard(models.Model):
    pdf = models.ForeignKey(PDFUpload, on_delete=models.CASCADE)
    flashcard_text = models.TextField()
