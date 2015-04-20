# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import hashers
from django.core.validators import validate_email
from django import forms
from account.forms import ArticleForm
import pprint


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
                    return render(request, 'account/sign_in.html', {'error': 'Konto nieaktywne!'})
            else:
                return render(request, 'account/sign_in.html', {'error': 'Błędny login lub hasło!'})
        return render(request, 'account/sign_in.html')
    else:
        return redirect('/account/edit/')


def lost_password(request):
    return render(request, 'account/lost_password.html')


def sign_out(request):
    logout(request)
    return redirect('spoleczni.views.index')


@login_required(login_url='/account/sign_in/')
def edit(request):
    articles = request.user.article_set.filter(public=True)
    return render(request, 'account/edit.html', {'articles': articles})


@login_required(login_url='/account/sign_in/')
def write_article(request):
    form = ArticleForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        pprint.pprint(form.author)
    return render(request, 'account/article.html', {'form': form, })


@login_required(login_url='/account/sign_in/')
def editform(request):
    errors = []
    success = []
    if request.method == 'POST':
        if 'change_password' in request.POST:
            password = request.POST.get('password')
            new_password = request.POST.get('new_password')
            repeat_new_password = request.POST.get('repeat_new_password')
            if password and new_password and repeat_new_password:
                if new_password != repeat_new_password:
                    errors.append('Nowe hasło niezgodne z powtórzeniem')
                else:
                    user = User.objects.get(username=request.user.get_username())
                    user_password = user.password

                    if hashers.check_password(password, user_password):
                        user.set_password(new_password)
                        user.save()
                        success.append('Hasło zostało zmienione pomyślnie')
                    else:
                        errors.append('Nieprawidłowe aktualne hasło')
            else:
                errors.append('Do zmiany hasła wymagane są wszystkie pola')
        else:
            user = User.objects.get(username=request.user.get_username())
            if request.POST.get('email'):
                try:
                    validate_email(request.POST.get("email", ""))
                    user.email = request.POST.get('email')
                except forms.ValidationError:
                    errors.append('Nieprawidłowy adres e-mail')

            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            success.append('Informacje o profilu zostały zapisane pomyślnie')

    user_data = User.objects.get(username=request.user.get_username())
    return render(
        request,
        'account/editform.html',
        {
            'user_data': user_data,
            'errors': errors,
            'success': success
        }
    )

@login_required
def messages(request):
    pass
