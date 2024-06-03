
from django.conf import settings
from django.template import loader
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist


def robots(request):

    sitemap_urls = []
    try:
        for sitemap_url in settings.ROBOTS_SITEMAP_URLS:
            sitemap_urls.append(f"{request.scheme}://{request.get_host()}{sitemap_url}")
    except AttributeError:
        pass

    context = {
        'scheme': request.scheme,
        'host': request.get_host(),
        'sitemap_urls': sitemap_urls,
    }

    template_name = f"robots/{settings.SERVER_ENV}.txt"
    try:
        loader.get_template(template_name)
    except TemplateDoesNotExist:
        template_name = "robots/default.txt"

    return render(request, template_name, context=context, content_type="text/plain")
