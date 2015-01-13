# -*- coding: utf-8 -*-
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(15, 5, label='Login:', required=True)
    password = forms.CharField(label='Hasło:', widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(label='Powtórz hasło:', widget=forms.PasswordInput(), required=True)
    email = forms.CharField(label='Email:', widget=forms.EmailInput(), required=True)
    first_name = forms.CharField(15, 5, label="Imię:", required=True)
    last_name = forms.CharField(15, 5, label="Nazwisko: ", required=True)
