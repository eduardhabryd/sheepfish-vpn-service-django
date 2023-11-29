from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic

from users.forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth import login, logout

from users.models import User


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('vpn_app:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('vpn_app:index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('vpn_app:index')


class UserUpdateView(generic.UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('vpn_app:index')
    template_name = 'registration/update.html'
