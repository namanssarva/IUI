from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import PDFUploadForm
from .models import PDFUpload, Question, Summary, Flashcard
import openai
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from PyPDF2 import PdfReader
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

openai.api_key = settings.OPENAI_API_KEY

def home(request):
    context = {}
    quote = get_motivational_quote()
    context['quote'] = quote
    return render(request, "index.html", context)

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                pdf_upload = form.save(commit=False)
                pdf_upload.user = request.user
                pdf_upload.save()
                request.session['pdf_id'] = pdf_upload.id  # Store pdf_id in session
                messages.success(request, "File uploaded successfully.")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = PDFUploadForm()
    return render(request, 'dashboard.html', {'form': form})

@login_required
def generate_content(request):
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        pdf_id = request.session.get('pdf_id')
        pdf_upload = PDFUpload.objects.get(id=pdf_id)
        text = extract_text_from_pdf(pdf_upload.pdf.path)

        if content_type == 'questions':
            content = generate_questions(text)
        elif content_type == 'summary':
            content = generate_summary(text)
        elif content_type == 'flashcards':
            content = generate_flashcards(text)
        else:
            return JsonResponse({'error': 'Invalid content type'}, status=400)

        return JsonResponse({'content': content})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_questions(text):
    chunks = chunk_text(text)
    questions = []
    for chunk in chunks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that generates questions."},
                {"role": "user", "content": f"Generate questions from the following text:\n\n{chunk}"}
            ]
        )
        questions_chunk = response['choices'][0]['message']['content'].strip().split('\n')
        questions.extend(questions_chunk)
    return questions

def generate_summary(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that generates summaries."},
            {"role": "user", "content": f"Generate a summary of the following text:\n\n{text}"}
        ]
    )
    return response['choices'][0]['message']['content']

def generate_flashcards(text):
    chunks = chunk_text(text)
    flashcards = []
    for chunk in chunks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that generates flashcards."},
                {"role": "user", "content": f"Generate flashcards from the following text:\n\n{chunk}"}
            ]
        )
        flashcards_chunk = response['choices'][0]['message']['content'].strip().split('\n')
        flashcards.extend(flashcards_chunk)
    return flashcards

def chunk_text(text, max_length=2048):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def get_motivational_quote():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that provides motivational quotes."},
            {"role": "user", "content": "Give me motivational quotes for studying with author names"}
        ],
        max_tokens=50,
        temperature=0.7,
        stop=["\n"]
    )
    return response['choices'][0]['message']['content'].strip()

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username.")
            return redirect('/login/')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid Password.")
            return redirect('/login/')
        else:
            auth_login(request, user)
            return redirect('/dashboard/')

    return render(request, "login.html", {})

def about(request):
    return render(request, "about.html", {})

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("POST DATA RECEIVED:", first_name, last_name, username, password)

        user = User.objects.filter(username=username)

        if not username or not password or not first_name or not last_name:
            messages.error(request, 'All fields are required')
            return redirect('/register/')

        if user.exists():
            messages.info(request, "Username already exists.")
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()

        messages.info(request, "Account Created Successfully.")
        return redirect('/login/')
    return render(request, 'register.html', {})

def logout_view(request):
    auth_logout(request)
    return redirect('/login/')
