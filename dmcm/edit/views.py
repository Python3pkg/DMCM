from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from dmcm.models import Page
from dmcm.edit.forms import PageForm


class PageCreateView(CreateView):
    template_name = 'dmcm/edit/page_detail.html'
    model = Page
    form_class = PageForm
    success_url = reverse_lazy('dmcm_edit_list_pages')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PageCreateView, self).dispatch(*args, **kwargs)
    

class PageUpdateView(UpdateView):
    template_name = 'dmcm/edit/page_detail.html'
    model = Page
    form_class = PageForm
    success_url = reverse_lazy('dmcm_edit_list_pages')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PageUpdateView, self).dispatch(*args, **kwargs)
