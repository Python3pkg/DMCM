"""Models used to store web pages."""

from django.db import models

class BlogPage(models.Model):
    """Page information for a blog entry.
    
    :Fields:
    
        date : date
            Date of blog entry.
        title : char
            Title of blog entry.
        filename : char
            Name of HTML and TXT files to which blog entry is written.
        updated : date_time
            When blog entry was last updated.
        body_markdown : text
            Blog entry body in markdown format.
        body : text
            Blog entry body in html format.
    """
    date = models.DateField()
    title = models.CharField(max_length=250, unique=True)
    filename = models.CharField(max_length=25, unique=True)
    updated = models.DateTimeField(verbose_name='Time Updated', auto_now=True)
    body_markdown = models.TextField(verbose_name='Blog entry body', help_text='Use Markdown syntax.')
    body = models.TextField(verbose_name='Blog entry body as HTML', blank=True, null=True)

    def save(self):
        """Convert markdown text into html and Save blog entry."""
        import markdown
        self.body = markdown.markdown(self.body_markdown, ['tables', 'toc',])
        #import smartypants
        #self.body = smartypants.smartyPants(self.body)
        super(BlogPage, self).save() # Call the "real" save() method.
    
    def __unicode__(self):
        return self.title

class Page(models.Model):
    """Page information.
    
    :Fields:
    
        title : char
            Title of page.
        dirname : char
            Name of directory to which HTML file is written.
        filename : char
            Name of HTML and TXT files to which page is written.
        parent : foreign_key on page
            Parent page in site structure.
        updated : date_time
            When page was last updated.
        body_markdown : text
            Page body in markdown format.
        body : text
            Page body in html format.
    """
    title = models.CharField(max_length=250, unique=True)
    dirname = models.CharField(max_length=25, blank=True)
    filename = models.CharField(max_length=25)
    parent = models.ForeignKey('self')
    updated = models.DateTimeField(verbose_name='Time Updated', auto_now=True)
    body_markdown = models.TextField(verbose_name='Page body', help_text='Use Markdown syntax.')
    body = models.TextField(verbose_name='Page body as HTML', blank=True, null=True)

    def save(self):
        """Convert markdown text into html and Save page."""
        import markdown
        self.body = markdown.markdown(self.body_markdown, ['tables', 'toc',])
        self.body = self.body.replace('<p> </p>', '')
        #import smartypants
        #self.body = smartypants.smartyPants(self.body)
        super(Page, self).save() # Call the "real" save() method.
    
    def __unicode__(self):
        return self.title

class List(models.Model):
    """List information.
    
    A list is a more structured form of page. Its body is generated from prefix and suffix
    text combined with cardgen output from a template and list of data items.
    
    :Fields:
    
        title : char
            Title of list.
        parent : foreign_key on page
            Parent page in site structure.
        updated : date_time
            When page was last updated.
        prefix : char
            First part of list.
        template : char
            Structure of a single item on list.
        delimiter : char
            Delimiter used to separate items in the data.
        data : text
            Data items separated by delimiters.
        suffix : char
            Last part of list.
        list_body : text
            List body in html format.
    """    
    title = models.CharField(max_length=250, unique=True)
    parent = models.OneToOneField(Page)
    updated = models.DateTimeField('Time Updated', auto_now=True)
    prefix = models.TextField(help_text='Use Markdown syntax.')
    template = models.TextField(help_text='Use Markdown syntax.')
    delimiter = models.CharField(max_length=1)
    data = models.TextField(help_text='Data items separated by delimiters.')
    suffix = models.TextField(help_text='Use Markdown syntax.')
    list_body = models.TextField(verbose_name='Generated', blank=True, null=True)

    def save(self):
        """Generate list from template and data.
        Combine results with prefix and suffix to create list_body."""
        list = self.prefix
        self.data = self.data.replace("\r","") #Remove any Linefeed chars
        data_lines = self.data.split("\n")
        data_header = data_lines[0].split(self.delimiter)
        print data_header
        num_labels = len(data_header)
        data_lines = data_lines[1:] # Remove header line
        for line in data_lines:
            data_fields = line.split(self.delimiter)
            next_item = self.template
            if len(data_fields) == len(data_header):
                # Replace labels in template with contents of equivalent data field
                for label_num, label in enumerate(data_header):
                    next_item = next_item.replace(label,data_fields[label_num])
            list = list + next_item
        self.list_body = list + self.suffix
        super(List, self).save() # Call the "real" save() method.

    def __unicode__(self):
        return self.title

class Option(models.Model):
    """Application Options.
    
    :Fields:
    
        deploy_path : char
            Fully qualified path to which directory html files are written when published.
        source_dir : char
            Name of directory within deployment directory to which markup source is written.
        nav_menu_body : text
            Html of site navigation menu.
        page_template : text
            Django template used to build site html files.
        root_page : 1-to-1 foreign_key
            Topmost page in site tree-structure.
        sitemap_list : 1-to-1 foreign_key
            List containing automatically generated site structure.
        blog_root_page : 1-to-1 foreign_key
            Topmost page of blog.
        blog_summary_size : int
            Number of blog entries to include on blog_root_page.
        blog_deploy_dir: char
            Directory to which blog html files are written when published.
        blog_source_dir : char
            Name of directory within blog deployment directory to which markup source is written.        sitemap_list : 1-to-1 foreign_key
    """
    deploy_path = models.CharField(max_length=250)
    source_dir = models.CharField(max_length=50)
    nav_menu_body = models.TextField()
    page_template = models.TextField()
    root_page = models.OneToOneField(Page)
    sitemap_list = models.OneToOneField(List)
    blog_root_page = models.OneToOneField(Page, related_name='blog_root')
    blog_summary_size = models.IntegerField()
    blog_deploy_dir = models.CharField(max_length=50)
    blog_source_dir = models.CharField(max_length=50)
   
    def __unicode__(self):
        return 'Options'
