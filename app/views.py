
from multiprocessing import context
from django.forms import PasswordInput
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as loginUser , logout
from app.forms import CRMForm , AuthenticationForm , RegistrationForm
from app.models import CRM
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

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
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email = email , password = password)
            if user is not None:
                loginUser(request,user)
                return redirect('home')
        else:
            form = AuthenticationForm()
            context = {
                "form" : form
                }
            return render(request , 'login.html' , context=context)



def signup(request):
    if request.method == 'GET':
        form = RegistrationForm()
        context = {
            "form" : form
        }
        return render(request , 'signup.html' , context=context)
    else:
        form = RegistrationForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate()
            if user is not None:
                return redirect('login')
        else:
            form = RegistrationForm()

        return render(request,'signup.html',{'form':form,})

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