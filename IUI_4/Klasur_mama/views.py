from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import DocumentForm
from .models import UploadedDocument
import openai
from django.conf import settings
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def home(request):
    return render(request, "home.html")

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

    # Generate PDF
    pdf_filename = f"{document_id}_output.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)
    generate_pdf(pdf_path, quiz, flashcard, summary)

    return JsonResponse({
        'quiz': quiz,
        'flashcard': flashcard,
        'summary': summary,
        'pdf_url': request.build_absolute_uri(f"/media/{pdf_filename}")
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

def generate_pdf(pdf_path, quiz, flashcard, summary):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, "Quiz")
    c.drawString(100, height - 120, quiz)

    c.drawString(100, height - 160, "Flashcards")
    c.drawString(100, height - 180, flashcard)

    c.drawString(100, height - 220, "Summary")
    c.drawString(100, height - 240, summary)

    c.save()
