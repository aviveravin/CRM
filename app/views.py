from multiprocessing import context
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as loginUser , logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm

from app.forms import CRMForm
from app.models import CRM
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    form = CRMForm
    crms = CRM.objects.all()
    return render(request , 'index.html' , context={'form' : form , 'crms' : crms})

def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            "form" : form
        }
        return render(request , 'login.html' , context=context)
    else:
        form = AuthenticationForm(data = request.POST)
        print(form.is_valid())
        print(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username , password = password)
            if user is not None:
                loginUser(request , user)
                return redirect('home')
        else:
            context = {
            "form" : form
            }
            return render(request , 'login.html' , context=context)

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form" : form
        }
        return render(request , 'signup.html' , context=context)
    else:
        form = UserCreationForm(request.POST)
        context = {
            "form" : form
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')    
        else:
            return render(request , 'signup.html' , context=context)
    

@login_required(login_url='login')
def add_job(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = CRMForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            crm = form.save(commit=False)
            crm.user = user
            crm.save()
            print(crm)
            return redirect("home")
        else:
            return render(request , 'index.html' , context={'form' : form})


def signout(request):
    logout(request)
    return redirect('login')