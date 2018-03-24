from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm

def signin(request):
    next = request.GET.get('next')
    title = "SIGN IN"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        if user.is_superuser:
            return redirect("dashboard")
        return redirect('/')
    return render(request, "accounts/form.html", {"form":form, "title": title})


def signup(request):
    next = request.GET.get('next')
    title = "SIGN UP"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "accounts/form.html", context)


def signout(request):
    logout(request)
    return redirect("/signin")

def profile(request):
    context = {'user': request.user}
    return render(request, 'accounts/profile.html', context)
