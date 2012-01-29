import os, shutil, ftplib, StringIO
import logging
# Usage: logging.debug(page.filename)

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import feedgenerator
from dmcm import settings
from dmcm.cm.models import BlogPage, Page, List, Option
from dmcm.cm.forms import BlogPageForm, PageForm, ListForm, OptionForm

@login_required
def blog_add(request):
    """Add blog entry.

    Display form to add blog entry details.

    Save entered data.
    """
    if request.method == 'POST': # If the form has been submitted...
        form = BlogPageForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            blog_page = form.save()
            return HttpResponseRedirect('/dmcm/blogupdt/' + str(blog_page.id))
    else:
        form = BlogPageForm()
    return render_to_response('blogadd.html',
                                {'form': form},
                                context_instance = RequestContext(request))

@login_required
def blog_update(request, blog_page_id):
    """Edit blog entry.
        
    :Parameters:
        
        blog_page_id : int
            Current blog entry.
        
    Display form with current blog entry details to be amended.

    Save entered data.
    """
    option = Option.objects.get(pk = 1)
    if request.method == 'POST': # If the form has been submitted...
        blog_page = BlogPage.objects.get(pk = blog_page_id)
        form = BlogPageForm(request.POST, instance = blog_page) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            if 'publish' in request.POST:
                publish_blog(blog_page)
            else:
                form.save()
    else:
        blog_page = BlogPage.objects.get(pk = blog_page_id)
        form = BlogPageForm(instance = blog_page)
    return render_to_response('blogupdt.html',
                                {'form': form, 'page': blog_page, 'option': option},
                                context_instance = RequestContext(request))

def publish_all():
    """Write all pages out as .html and .txt files."""
    option = Option.objects.get(pk = 1)
    site = Site.objects.get_current()
    ftp_serv = ftplib.FTP(settings.FTP_HOST, settings.FTP_USERNAME, settings.FTP_PASSWORD)
    pages = Page.objects.all()
    for page in pages:
        rendered = render_to_string("main.html", {'page': page,
                                                    'site': site,
                                                    'navmenu': option.nav_menu_body})
        file = StringIO.StringIO(rendered)
        ftpfilename = option.deploy_path + page.dirname + page.filename + ".html"
        resp = ftp_serv.storlines("STOR " + ftpfilename, file)
        file = StringIO.StringIO(page.body_markdown)
        ftpfilename = option.deploy_path + page.dirname + option.source_dir + page.filename + ".txt"
        resp = ftp_serv.storlines("STOR " + ftpfilename, file)
    pages = BlogPage.objects.all()
    for page in pages:
        rendered = render_to_string("main.html", {'page': page,
                                                    'site': site,
                                                    'blog' : True,
                                                    'navmenu': option.nav_menu_body})
        ftp_serv = ftplib.FTP(settings.FTP_HOST, settings.FTP_USERNAME, settings.FTP_PASSWORD)
        file = StringIO.StringIO(rendered)
        ftpfilename = option.deploy_path + option.blog_deploy_dir + \
            page.date.isoformat() + "-" + page.filename + ".html"
        resp = ftp_serv.storlines("STOR " + ftpfilename, file)
        file = StringIO.StringIO(page.body_markdown)
        ftpfilename = option.deploy_path + option.blog_deploy_dir + option.blog_source_dir + \
            page.date.isoformat() + "-" + page.filename + ".txt"
        resp = ftp_serv.storlines("STOR " + ftpfilename, file)
    publish_blog_summary(ftp_serv)
    ftp_serv.close

def publish_blog(blog_page):
    """Write blog entry out as .html and .txt files."""
    option = Option.objects.get(pk = 1)
    site = Site.objects.get_current()
    rendered = render_to_string("main.html", {'page': blog_page,
                                                'site': site,
                                                'blog' : True,
                                                'navmenu': option.nav_menu_body})
    ftp_serv = ftplib.FTP(settings.FTP_HOST, settings.FTP_USERNAME, settings.FTP_PASSWORD)
    file = StringIO.StringIO(rendered)
    ftpfilename = option.deploy_path + option.blog_deploy_dir + \
        blog_page.date.isoformat() + "-" + blog_page.filename + ".html"
    resp = ftp_serv.storlines("STOR " + ftpfilename, file)
    file = StringIO.StringIO(blog_page.body_markdown)
    ftpfilename = option.deploy_path + option.blog_deploy_dir + option.blog_source_dir + \
        blog_page.date.isoformat() + "-" + blog_page.filename + ".txt"
    resp = ftp_serv.storlines("STOR " + ftpfilename, file)
    publish_blog_summary(ftp_serv)
    ftp_serv.close

def publish_blog_summary(ftp_serv):
    """Write recent blog entries out in a .html file.
    
    Also write .rss file for all entries.
    """
    option = Option.objects.get(pk = 1)
    site = Site.objects.get_current()
    page = Page.objects.get(pk = option.blog_root_page.id)
    page.body_markdown = 'Blog: [Archive](#archive "Older Blog Entries");\n' + \
        '[RSS](http://dmcm-site/dmcm/rss "RSS feed of recent blog entries").\n\n'
    # Include recent entries
    blog_entries = BlogPage.objects.all().order_by('-date', 'title')[:option.blog_summary_size]
    for blog_entry in blog_entries:
        page.body_markdown = page.body_markdown + "## " + blog_entry.title + "\n\n"
        page.body_markdown = page.body_markdown + "*Published: " + \
            blog_entry.date.strftime("%d %B %Y") + "*\n"
        page.body_markdown = page.body_markdown + \
            "[Comment](" + blog_entry.date.isoformat() + \
            "-" + blog_entry.filename + ".html)\n\n"
        page.body_markdown = page.body_markdown + blog_entry.body_markdown + "\n\n"
    # Include archive of all entries
    blog_entries = BlogPage.objects.all().order_by('-date', 'title')
    page.body_markdown = page.body_markdown + '<p><a href="#">Back to Top</a></p>\n'
    page.body_markdown = page.body_markdown + '<h2 id="archive">Archive</h2>\n\n'
    page.body_markdown = page.body_markdown + "Date | Title | View\n-----|------|-----\n"
    for blog_entry in blog_entries:
        page.body_markdown = page.body_markdown + blog_entry.date.isoformat() + " | " + \
            blog_entry.title + " | [View](" + \
            blog_entry.date.isoformat() + "-" + blog_entry.filename + ".html)\n"
    page.body_markdown = page.body_markdown + '\n<p><a href="#">Back to Top</a></p>\n'
    page.save()
    rendered = render_to_string("main.html", {'page': page,
                                                'site': site,
                                                'navmenu': option.nav_menu_body})
    file = StringIO.StringIO(rendered)
    ftpfilename = option.deploy_path + option.blog_deploy_dir + "index.html"
    resp = ftp_serv.storlines("STOR " + ftpfilename, file)
    file = StringIO.StringIO(page.body_markdown)
    ftpfilename = option.deploy_path + option.blog_deploy_dir + option.blog_source_dir + \
                                        "index.txt"
    resp = ftp_serv.storlines("STOR " + ftpfilename, file)


def publish_page(page):
    """Write page out as .html and .txt files."""
    option = Option.objects.get(pk = 1)
    site = Site.objects.get_current()
    rendered = render_to_string("main.html", {'page': page,
                                                'site': site,
                                                'navmenu': option.nav_menu_body})
    ftp_serv = ftplib.FTP(settings.FTP_HOST, settings.FTP_USERNAME, settings.FTP_PASSWORD)
    file = StringIO.StringIO(rendered)
    ftpfilename = option.deploy_path + page.dirname + page.filename + ".html"
    resp = ftp_serv.storlines("STOR " + ftpfilename, file)
    file = StringIO.StringIO(page.body_markdown)
    ftpfilename = option.deploy_path + page.dirname + option.source_dir + page.filename + ".txt"
    resp = ftp_serv.storlines("STOR " + ftpfilename, file)
    ftp_serv.close

def generate_site_map():
    """Generate Site Map from pages of site."""
    global node_list

    class Node:
        def __init__(self, node, title, filename):
            self.id = node
            self.title = title
            self.filename = filename
            self.level = 0
            self.children = []

    def walk_tree(node, lvl = 0, visited = []):
        if node in visited:
            # Cycle detected.
            return
        else:
            node.level = lvl
            visited.append(node)
        for n in node.children:
            visited = walk_tree(n, lvl + 1, visited)
        return visited

    treeMap = {}
    option = Option.objects.get(pk = 1)
    root_page = Page.objects.get(pk = option.root_page.id)
    Root = Node(root_page.id, root_page.title, root_page.filename)
    treeMap[Root.id] = Root
    pages = Page.objects.all().order_by('parent', 'title').exclude(pk = Root.id)
    for page in pages:
        if not page.id in treeMap:
            treeMap[page.id] = Node(page.id, page.title, page.filename)
        else:
            treeMap[page.id].id = page.id
            treeMap[page.id].title = page.title
            treeMap[page.id].filename = page.filename
        if not page.parent.id in treeMap:
            treeMap[page.parent.id] = Node(0, '', '')
        treeMap[page.parent.id].children.append(treeMap[page.id])
    node_list = "#Level,#Title,#Filename"
    nodes = walk_tree(Root)
    for n in nodes:
        node_list += "\n" + str(n.level) + "," + n.title + "," + n.filename
    site_map = option.sitemap_list
    site_map.data = node_list
    site_map.save()
    return site_map


@login_required
def home(request):
    """Show Blog Entries, Pages and Lists which make up site."""
    blog_entries = BlogPage.objects.all().order_by('-date', 'title')
    pages = Page.objects.all().order_by('parent', 'title')
    lists = List.objects.all().order_by('parent', 'title')
    return render_to_response('home.html', {'pages': pages,
                                            'lists': lists,
                                            'blog_entries' : blog_entries})

@login_required
def list_add(request):
    """Add List.

    Display form to enter list details.

    Save entered data.
    """
    if request.method == 'POST': # If the form has been submitted...
        form = ListForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            list = form.save()
            return HttpResponseRedirect('/dmcm/listupdt/' + str(list.id))
    else:
        form = ListForm()
    return render_to_response('listadd.html',
                                {'form': form},
                                context_instance = RequestContext(request))

@login_required
def list_update(request, list_id):
    """Edit List.
        
    :Parameters:
        
        list_id : int
            Current list.
        
    Display form with current list details to be amended.

    Save entered data.
    """
    if request.method == 'POST': # If the form has been submitted...
        list = List.objects.get(pk = list_id)
        form = ListForm(request.POST, instance = list) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
    else:
        list = List.objects.get(pk = list_id)
        form = ListForm(instance = list)
    return render_to_response('listupdt.html',
                                {'form': form,
                                'list': list,
                                'parent_id': list.parent_id},
                                context_instance = RequestContext(request))

@login_required
def options(request):
    """Update Options."""

    if request.method == 'POST': # If the form has been submitted...
        option = Option.objects.get(pk = 1)
        sitemap = List.objects.get(pk = option.sitemap_list.id)
        form = OptionForm(request.POST, instance = option) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            if 'publish' in request.POST:
                publish_all()
            elif 'sitemap' in request.POST:
                list = generate_site_map()
                return HttpResponseRedirect('/dmcm/listupdt/' + str(list.id))
            elif 'pagetemplate' in request.POST:
                form.save()
                # Write (FTP) page template file
                ftp_serv = ftplib.FTP(settings.FTP_HOST, settings.FTP_USERNAME, settings.FTP_PASSWORD)
                file = StringIO.StringIO(option.page_template)
                ftpfilename = settings.FTP_TEMPLATE_DIR + '/' + settings.MAIN_TEMPLATE
                resp = ftp_serv.storlines("STOR " + ftpfilename, file)
                ftp_serv.close
            else:
                form.save()
    else:
        option = Option.objects.get(pk = 1)
        sitemap = List.objects.get(pk = option.sitemap_list.id)
        form = OptionForm(instance = option)
    return render_to_response('options.html',
                                {'form': form, 'sitemap': sitemap},
                                context_instance = RequestContext(request))

@login_required
def page_add(request):
    """Add Page.

    Display form to enter page details.

    Save entered data.
    """
    if request.method == 'POST': # If the form has been submitted...
        form = PageForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            page = form.save()
            return HttpResponseRedirect('/dmcm/pageupdt/' + str(page.id))
    else:
        form = PageForm()
    return render_to_response('pageadd.html',
                                {'form': form},
                                context_instance = RequestContext(request))

@login_required
def page_update(request, page_id):
    """Edit Page.
        
    :Parameters:
        
        page_id : int
            Current page.
        
    Display form with current page details to be amended.

    Save entered data.
    """

    if request.method == 'POST': # If the form has been submitted...
        page = Page.objects.get(pk = page_id)
        try:
            list = List.objects.get(parent__exact = page_id)
        except List.DoesNotExist:
            list = None
        form = PageForm(request.POST, instance = page) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            if 'replace' in request.POST:
                page.body_markdown = list.list_body
                form = PageForm(instance = page)
            elif 'publish' in request.POST:
                publish_page(page)
            else:
                form.save()
    else:
        page = Page.objects.get(pk = page_id)
        try:
            list = List.objects.get(parent__exact = page_id)
        except List.DoesNotExist:
            list = None
        form = PageForm(instance = page)
    return render_to_response('pageupdt.html',
                                {'form': form, 'page': page, 'list': list},
                                context_instance = RequestContext(request))
