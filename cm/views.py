from django.shortcuts import render_to_response, get_object_or_404

from dmcm.cm.models import Page

def page(request, page_id):
    """Show Blog Entries, Pages and Lists which make up site."""
    page = get_object_or_404(Page, pk=page_id)
    context = {'page': page,}
    return render_to_response('page.html', context)

def site_map(request):
    """Build Site Map to display."""
    pages = Page.objects.all()
    site_map = '# Site Map\n\nPage Title | Parent | Updated\n-----|-----|-----\n'
    for page in pages:
        site_map += '['+page.title+'](/page/'+str(page.id)+') | '
        site_map += page.parent.title+' | '+page.updated.strftime("%Y-%m-%d %H:%M")+'\n'
    context = {'site_map': site_map,}
    return render_to_response('site_map.html', context)

def search_pages(request):
    search_string = request.GET.get('search_string', '')
    if len(search_string) < 3:
        return render_to_response('search_results.html', {'search_string': search_string, 'too_small': True})
    title_match_pages = Page.objects.filter(title__icontains=search_string)
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
            match_pos = content_lower.find(search_string_lower, match_pos+1)
        content_matches.append({'page': page, 
                                'matching_lines': matching_lines, 
                                'number_found': number_found,
                            })
    context = {'title_match_pages': title_match_pages,
               'content_matches': content_matches,
               'search_string': search_string,
    }
    return render_to_response('search_results.html', context)