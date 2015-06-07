from django import forms
from articles.models import Category
from articles.models import Article
from django.contrib.auth.models import User



# FILTROWANIE
class ArticleFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ArticleFilterForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            queryset=Category.objects.all(),
            required=False,
            label="Kategoria"
        )
        self.fields['date'] = forms.DateTimeField(
            widget=forms.DateInput(attrs={'class': 'form-control datepicker'}),
            required=False,
            label="Data"
        )
        self.fields['author']=forms.ModelChoiceField(
            widget=forms.Select(attrs={'class': 'form-control'}),
            queryset = User.objects.all()  ,
            required=False,
            label="Autor"
        )



# WYSZUKIWANIE
class ArticleSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ArticleSearchForm, self).__init__(*args, **kwargs)
        self.fields['query'] = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            required=False,
            label="Szukaj"
        )


# Tagi
class ArticleTagsForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['tags', ]