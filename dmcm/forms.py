from django import forms

class StringSearchForm(forms.Form):
    search_string = forms.CharField()