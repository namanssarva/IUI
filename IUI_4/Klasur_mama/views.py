from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import DocumentForm
from .models import UploadedDocument
import os
import openai
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required





context ={}
# Create your views here.
def home(request):

    context ={}
    api_key = os.getenv("Your api")
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
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo-1106",
        messages=[
                {"role": "system", "content": "You are an AI that provides motivational quotes."},
                {"role": "user", "content": "give me motivational quotes for setudying with author names"}
            ],
        max_tokens=50,
        temperature=0.7,
        stop=["\n"]
    )
    return response.choices[0].message.content.strip()
    
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username ).exists():

            messages.error(request, "Invalid Username.")
            return redirect('/login/')
        user = authenticate(username = username, password = password)
        if user is None:
            messages.error(request, "Invalid Password.")
            return redirect('/login/')
        else:
            login(request , user)
            return redirect('/dashboard/')



    return render(request,"login.html", context)
def about(request):
    return render(request,"about.html", context)

def register(request):
    if request.method =="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if not username or not password or not first_name or not last_name:
            messages.error(request, 'All fields are required')
            return redirect('/register/')


        if user.exists():
            messages.info(request, "Username already exists.")
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save()

        messages.info(request, "Account Created Sucessfully.")

        return redirect('/register/')
    return render (request, 'register.html',context)
