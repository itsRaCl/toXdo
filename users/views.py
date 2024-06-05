from django.contrib.auth import logout 
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegistrationForm

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        messages.error(request,"You can't access this page!")
        return redirect("main:home")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            messages.success(request,"User created! You can now login!")
            return redirect("users:login")
        else:
            messages.error(request, "Something went wrong!")

    form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully!")
    return redirect("users:login")
