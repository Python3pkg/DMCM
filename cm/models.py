"""Models used to store web pages."""
from django.db import models

class Page(models.Model):
    """Page information.
    
    :Fields:
    
        title : char
            Title of page.
        parent : foreign_key on page
            Parent page in site structure.
        updated : date_time
            When page was last updated.
        content : text
            Page content in markdown format.
    """
    title = models.CharField(max_length = 250, unique = True)
    parent = models.ForeignKey('self')
    published = models.DateField(null=True,blank=True)
    updated = models.DateTimeField(verbose_name = 'Time Updated', auto_now = True)
    content = models.TextField(verbose_name = 'Page body', help_text = 'Use Markdown syntax.')
    wide = models.BooleanField(verbose_name = 'Wider Page')

    def navigation_path(self):
        path = []
        parent = self.parent
        if parent != self:
            while parent != parent.parent:
                path.insert(0, {'title': parent.title, 'address': '/page/'+str(parent.id)+'/'})
                parent = parent.parent
            path.insert(0, {'title': parent.title, 'address': '/'})
        return path

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title