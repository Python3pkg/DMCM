from django import forms
from dmcm.cm.models import BlogPage, Page, List, Option

class BlogPageForm(forms.ModelForm):
    """Add/Update blog entry contents.
    
    :Fields:
    
        date : date
            
        title : char
            
        filename : char
            
        body_markdown : text
            Blog entry entered in markdown format.
    """
    date = forms.DateField()
    title = forms.CharField()
    filename = forms.CharField()
    body_markdown = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':30,'cols':80}))
    
    class Meta:
        model = BlogPage
        fields = ['date', 'title', 'filename', 'body_markdown']

class PageForm(forms.ModelForm):
    """Add/Update Page contents.
    
    :Fields:
    
        title : text

        dirname : text

        filename : text
        
        parent : Choose any Page
            Choice field based on entries in Page model.
        body_markdown : text
            Page contents entered in Markdown format.
    """
    title = forms.CharField()
    dirname = forms.CharField(required=False)
    filename = forms.CharField()
    parent = forms.ModelChoiceField(queryset=Page.objects.all(), empty_label=None)
    body_markdown = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':30,'cols':80}))
    
    class Meta:
        model = Page
        fields = ['title', 'dirname', 'filename', 'parent', 'body_markdown']

class ListForm(forms.ModelForm):
    """Add/Update List contents.
    
    :Fields:
    
        title : text

        parent : Choose any Page
            Choice field based on entries in Page model.
        prefix : text
            Text before List contents, entered in Markdown format.
        template : text
            Structure of List contents.
        delimiter : text
            Separator of fields on each line of data.
        data : text
            List contents, fields separated by delimiters.
        suffix : text
            Text after List contents, entered in Markdown format.
    """
    title = forms.CharField()
    parent = forms.ModelChoiceField(queryset=Page.objects.all(), empty_label=None)
    prefix = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':6,'cols':80}))
    template = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':2,'cols':80}))
    delimiter = forms.CharField(max_length=1)
    data = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':30,'cols':80}))
    suffix = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':2,'cols':80}))
    body_markdown = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':30,'cols':80}))
    
    class Meta:
        model = List
        fields = ['title', 'parent', 'prefix', 'template', 'delimiter', 'data', 'suffix']

class OptionForm(forms.ModelForm):
    """Update Options."""
    deploy_path = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
    nav_menu_body = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':30,'cols':80}))
    page_template = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':30,'cols':80}))

    class Meta:
        model = Option
