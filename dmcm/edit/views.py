from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView

from ..models import Page
from ..edit.forms import PageForm


class PageCreateView(CreateView):
    template_name = 'dmcm/edit/page_detail.html'
    model = Page
    form_class = PageForm
    
    def get_success_url(self): 
        return reverse('dmcm_page_detail',args=(self.object.slug,))
    
    
class PageUpdateView(UpdateView):
    template_name = 'dmcm/edit/page_detail.html'
    model = Page
    form_class = PageForm
    
    def get_success_url(self):
        return reverse('dmcm_page_detail', args=(self.object.slug,))
