from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import DocumentForm
from .models import UploadedDocument
import os
import openai
from django.conf import settings

# Create your views here.
def home(request):
    return render(request, "website/index.html")


openai.api_key = settings.OPENAI_API_KEY

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            return redirect('process_document', document_id=document.id)
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})

def process_document(request, document_id):
    document = UploadedDocument.objects.get(id=document_id)
    file_path = document.file.path

    # Read the content of the file
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Generate quiz, flashcard, and summary using OpenAI API
    quiz = generate_quiz(file_content)
    flashcard = generate_flashcard(file_content)
    summary = generate_summary(file_content)

    return JsonResponse({
        'quiz': quiz,
        'flashcard': flashcard,
        'summary': summary
    })

def generate_quiz(content):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate a quiz based on the following content:\n\n{content}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_flashcard(content):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate flashcards based on the following content:\n\n{content}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_summary(content):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following content:\n\n{content}",
        max_tokens=150
    )
    return response.choices[0].text.strip()