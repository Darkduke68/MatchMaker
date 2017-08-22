from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import RegisterForm


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('questions')
    else:
        return render(request, 'registration/register.html', {'form': form})
