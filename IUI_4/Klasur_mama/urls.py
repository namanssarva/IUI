from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_document, name='upload_document'),
    path('process/<int:document_id>/', views.process_document, name='process_document'),
]
