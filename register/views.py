from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from osa import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text


# Create your views here.

def about(request):
    return render(request, "register/about.html")

    
def home(request):
    return render(request, "register/index.html")


def signup(request):

    if  request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        if User.objects.filter(username=username):
            messages.error(request, "username already exists")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already exists")
            return redirect('home')

        if len(username)>15:
            messages.error(request, "Username must be under 15 characters")

        if pass1 != pass2:
            messages.error(request, "Passwords didnt match")

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")
            return redirect('home')

        myuser = User.objects.create_user(username, email,  pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        

        myuser.save()

        messages.success(request, "Succesfully signedup")


        return redirect('signin')



    return render(request, "register/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "register/index.html", {'fname': fname})

        else:
            messages.error(request, "Invalid email or password")
            return redirect('home')




    return render(request, "register/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "LoggedOut Successfully")
    return redirect('home')


