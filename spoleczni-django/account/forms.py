# -*- coding: utf-8 -*-
from django import forms
from articles.models import Article
from ckeditor.widgets import CKEditorWidget


class RegisterForm(forms.Form):
    username = forms.CharField(15, 5, label='Login:', required=True)
    password = forms.CharField(label='Hasło:', widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(label='Powtórz hasło:', widget=forms.PasswordInput(), required=True)
    email = forms.CharField(label='Email:', widget=forms.EmailInput(), required=True)
    first_name = forms.CharField(15, 5, label="Imię:", required=True)
    last_name = forms.CharField(15, 5, label="Nazwisko: ", required=True)


class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control'}))

    class Meta:
        model = Article
        fields = ['title', 'category', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        self.author = user
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = 'Treść'