from django.conf import settings
from django.contrib.sites.models import Site

site = Site.objects.get_current()

def context_processor(request):
    """
    Add values to the context of all templates.
    """
    return {'DEVELOP': settings.DEVELOP,
            'SITE_ROOT_ID': settings.SITE_ROOT_ID,
            'BLOG_ROOT_ID': settings.BLOG_ROOT_ID,
            'site': site
            }
