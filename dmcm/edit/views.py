from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from dmcm.models import Page
from dmcm.edit.forms import PageForm


class PageCreateView(CreateView):
    template_name = 'dmcm/edit/page_detail.html'
    model = Page
    form_class = PageForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PageCreateView, self).dispatch(*args, **kwargs)
    
    def get_success_url(self): 
        return reverse('dmcm_page_detail',args=(self.object.slug,))
    
    
class PageUpdateView(UpdateView):
    template_name = 'dmcm/edit/page_detail.html'
    model = Page
    form_class = PageForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PageUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('dmcm_page_detail', args=(self.object.slug,))
