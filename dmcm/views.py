from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import ListView
from django.conf import settings
from dmcm.forms import StringSearchForm
from dmcm.models import Page


class WideListView(ListView):
    """
    Add extra context value 'object.wide'. Gets base template to make content area wider.
    """
    def get_context_data(self, **kwargs):
        context = super(WideListView, self).get_context_data(**kwargs)
        context['object'] = {'wide': True}
        return context


def search_pages(request):
    """
    Simple string search.

    Display pages with titles and/or content which contain the string searched for.
    """
    form = StringSearchForm(request.GET)
    search_string = form.cleaned_data['search_string'] if form.is_valid() else ''
    if len(search_string) < 3:
        return render_to_response('dmcm/search_results.html',
                                  {'search_string': search_string, 'too_small': True},
                                  RequestContext(request))
    title_matches = Page.objects.filter(title__icontains=search_string)
    content_match_pages = Page.objects.filter(content__icontains=search_string)
    content_matches = []
    search_string_lower = search_string.lower()
    for page in content_match_pages:
        content_lower = page.content.lower()
        number_found = content_lower.count(search_string_lower)
        # Display each line containing matches only once.
        matching_lines = []
        match_pos = content_lower.find(search_string_lower)
        while match_pos > 0:
            prev_newline = content_lower.rfind('\n', 0, match_pos)
            next_newline = content_lower.find('\n', match_pos)
            if prev_newline > 0 and next_newline > 0:
                matching_line = page.content[prev_newline:next_newline]
            elif prev_newline < 0 and next_newline > 0:
                matching_line = page.content[0:next_newline]
            elif  prev_newline > 0 and next_newline < 0:
                matching_line = page.content[prev_newline:]
            else:
                matching_line = page.content
            matching_lines.append(matching_line)
            match_pos = content_lower.find(search_string_lower, next_newline) if next_newline > 0 else -1
        content_matches.append({'page': page,
                                'matching_lines': matching_lines,
                                'number_found': number_found})
    context = {'title_matches': title_matches,
               'content_matches': content_matches,
               'search_string': search_string,
               'object': {'wide': True}}  # Dispplay results in a wide content area on page.
    return render_to_response('dmcm/search_results.html', context, RequestContext(request))

TOOL_NAMES = ['cardgen', 'deduplicate', 'compare']


def show_tool(request, tool_name=""):
    """
    Render template containing requested (javascript) tool.
    """
    context = {}
    if tool_name in TOOL_NAMES:
        template = 'dmcm/tool_%s.html' % (tool_name)
        return render_to_response(template, context, RequestContext(request))
    else:
        raise Http404


@login_required
def edit_page(request, slug=""):
    """
    Redirect edit requests to Admin.
    """
    page = get_object_or_404(Page, slug=slug)
    return redirect(reverse('admin:dmcm_page_change', args=(page.id,)))


@login_required
def server_status_dashboard(request):
    """
    Build page providing information about the state of the system.
    """
    import django
    import reversion
    import markdown
    import os
    from subprocess import Popen, PIPE

    # Shell commands: Name and command
    SHELL_COMMANDS = [
        ('hostname', 'hostname'),
        ('gitversion', 'git log -n 1'),
        ('mysql_version', 'mysql --version'),
    ]

    # Flags in settings: Their expected  and actual values.
    SETTINGS_FLAGS = [
        ('DEBUG', False),
        ('DEVELOP', False),
    ]

    def run_shell_command(command, cwd):
        """
        Run command in shell and return results.
        """
        p = Popen(command, shell=True, cwd=cwd, stdout=PIPE)
        stdout = p.communicate()[0]
        if stdout:
            stdout = stdout.strip()
        return stdout

    context = {'object': {'wide': True}}

    # Versions
    context['django_version'] = '.'.join(str(i) for i in django.VERSION)
    context['markdown_version'] = '.'.join(str(i) for i in markdown.version_info)
    context['reversion_version'] = '.'.join(str(i) for i in reversion.VERSION)

    curr_dir = os.path.realpath(os.path.dirname(__file__))
    for name, shell_command in SHELL_COMMANDS:
        context[name] = run_shell_command(shell_command, curr_dir)

    # Settings Flags
    context['settings_flags'] = []
    for name, expected in SETTINGS_FLAGS:
        actual_setting = getattr(settings, name, None)
        context['settings_flags'].append({
            'name': name,
            'unexpected': expected != actual_setting,
            'actual': actual_setting
        })

    context['time_checked'] = datetime.now()
    return render_to_response('server_status_dashboard.html', context, RequestContext(request))
