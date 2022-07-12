from django.contrib.sites.models import Site


def site(request):
    ctx = {}

    if Site._meta.installed:
        site = Site.objects.get_current(request)
        ctx.update({
            'SITE_NAME': site.name,
            'SITE_DOMAIN': site.domain
        })

    return ctx
