from project.settings import DEVELOP, SITE_ROOT_ID, BLOG_ROOT_ID

def context_processor(request):
    """
    Add values to the context of all templates.
    """
    return {'DEVELOP': DEVELOP, 
            'SITE_ROOT_ID': SITE_ROOT_ID,
            'BLOG_ROOT_ID': BLOG_ROOT_ID}
