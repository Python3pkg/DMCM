from django import forms


class StringSearchForm(forms.Form):
    """
    Allow user to enter a string to search the for matching entries.
    """
    search_string = forms.CharField()
