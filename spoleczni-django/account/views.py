# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import forms


def register(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                new_user = register_form.save()
                return redirect("/account/sign_in")
        else:
            register_form = UserCreationForm()
        return render(request, "account/register.html", {
            'register_form': register_form,
        })
    else:
        return redirect('/account/edit')


def sign_in(request):
    if not request.user.is_authenticated():
        if 'log_in' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('spoleczni.views.index')
                else:
                    return render(request, 'account/sign_in.html', {'error':'Konto nieaktywne!'})
            else:
                return render(request, 'account/sign_in.html', {'error':'Błędny login lub hasło!'})
        return render(request, 'account/sign_in.html')
    else:
        return redirect('/account/edit/')


def lost_password(request):
    return render(request, 'account/lost_password.html')


def sign_out(request):
    logout(request)
    return redirect('spoleczni.views.index')


@login_required(login_url='/accounts/sign_in/')
def edit(request):
    return render(request, 'account/edit.html')
