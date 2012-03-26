from dmcm.settings import DEBUG, SITE_ROOT_ID

def context_processor(request):
    return {'DEBUG': DEBUG, 'SITE_ROOT_ID': SITE_ROOT_ID}