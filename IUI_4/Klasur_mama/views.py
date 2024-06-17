from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import DocumentForm
from .models import UploadedDocument
import os
import openai
from django.conf import settings
context ={}
# Create your views here.
def home(request):

    context ={}
    api_key = os.getenv("YOUR_API_KEY")
    print(f"API Key : {api_key}")

    quote = get_motivational_quote()
    context['quote'] = quote
    return render(request, "index.html",context)


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
    response = openai.completions.create(
        model="davinci-002",
        prompt=f"Generate a quiz based on the following content:\n\n{content}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_flashcard(content):
    response = openai.completions.create(
        model="davinci-002",
        prompt=f"Generate flashcards based on the following content:\n\n{content}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_summary(content):
    response = openai.completions.create(
        model="davinci-002",
        prompt=f"Summarize the following content:\n\n{content}",
        max_tokens=150
    )
    return response.choices[0].text.strip()
def get_motivational_quote():
    response = openai.completions.create(
        model = "davinci-002",
        prompt = "Give me motivational quotes for studying.",
        max_tokens=50,
        stop=["\n"]
    )
    return response.choices[0].text.strip()
def login(request):
    context ={}
    return render(request,"login.html", context)
def about(request):
    return render(request,"about.html", context)