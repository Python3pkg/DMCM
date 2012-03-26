from django.shortcuts import render_to_response
from django.template import RequestContext

from dmcm.cm.models import Page
from dmcm.cm.forms import StringSearchForm

def search_pages(request):
    form = StringSearchForm(request.GET)
    search_string = form.cleaned_data['search_string'] if form.is_valid() else ''
    if len(search_string) < 3:
        return render_to_response('cm/search_results.html', 
                                  {'search_string': search_string, 'too_small': True},
                                  RequestContext(request))
    title_matches = Page.objects.filter(title__icontains=search_string)
    content_match_pages = Page.objects.filter(content__icontains=search_string)
    content_matches = []
    search_string_lower = search_string.lower()
    for page in content_match_pages:
        content_lower = page.content.lower()
        number_found = content_lower.count(search_string_lower)
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
                                'number_found': number_found,
                            })
    context = {'title_matches': title_matches,
               'content_matches': content_matches,
               'search_string': search_string,
    }
    return render_to_response('cm/search_results.html', context, RequestContext(request))