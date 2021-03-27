from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def Signup(request):
    context = {
        'reg_errors': [],
    }
    if request.method == "POST":
        if len(request.POST['pass1']) >= 8:
            if request.POST['pass1'] == request.POST['pass2']:
                if User.objects.filter(email=request.POST['email']).exists():
                    context["reg_errors"].append("Email already in use!")
                else:
                    email=request.POST['email']
                    pass1=request.POST['pass1']
                    myuser = User.objects.create_user(
                    username=email,
                    email=email,
                    password=pass1
                    )
                    myuser.save()
                    messages.success(request, "Your Account has been successfully Created")
                    return redirect("accounts:login")
            else:
                context["reg_errors"].append("Passwords don't match!")
        else :
            context["reg_errors"].append("Password Length Should be Greater than 8!")
    return render(request,"accounts/signup.html", context)



def Login(request):
    context = {}
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("Home:home")
        else:
            context['login_error'] = "Invalid credentials!"
    return render(request,"accounts/login.html", context)

def Logout(request):
    logout(request)
    return redirect("Home:home")
