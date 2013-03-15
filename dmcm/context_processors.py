from django.conf import settings


def context_processor(request):
    """
    Add values to the context of all templates.
    """
    return {'DEVELOP': settings.DEVELOP,
            'SITE_ROOT_ID': settings.SITE_ROOT_ID,
            'BLOG_ROOT_ID': settings.BLOG_ROOT_ID}
