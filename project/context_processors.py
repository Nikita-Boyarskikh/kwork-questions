from django.contrib.sites.shortcuts import get_current_site


def site(request):
    current_site = get_current_site(request)
    return {
        'SITE_NAME': current_site.name,
        'SITE_DOMAIN': current_site.domain
    }
