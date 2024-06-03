# Django Env Robots (.txt)

Serve different robots.txt from your production | stage | etc servers by setting environment variables. Rules are managed via templates.
By default it excludes robots entirely.


## Installation

Install from [PyPI](https://pypi.org/project/django-env-robots/):

```
pip install django-env-robots
```

Then add the following to your project's `INSTALLED_APPS`.

```
'django_env_robots',
```

## Usage

### settings.py
Set the following:
 - `SERVER_ENV` identifies the nature of the server and thus the robots.txt template that will be used.
 - `ROBOT_SITEMAP_URLS` a list of relative urls to your sitemap(s).

E.g:
```
SERVER_ENV = 'production'
ROBOTS_SITEMAP_URLS = ['/sitemap.xml', '/other_sitemap.xml']
```

### urls.py
```
from django_env_robots import urls as robots_urls
...
urlpatterns = [
    path("robots.txt", include(robots_urls)),
]
```

### robots templates
Create corresponding template files for each SERVER_ENV you will be using.
These live in your projects `templates` directory in a `robots` subfolder.

For example, if `SERVER_ENV` can be `production` or `stage`, then create:
 - `templates/robots/production.txt`
 - `templates/robots/stage.txt`

e.g:
```
User-agent: *
Disallow: /admin/*

{% for sitemap_url in sitemap_urls %}Sitemap: {{ sitemap_url }}
{% endfor %}
```

### Other considertions

A robots.txt being served from a Whitenose public directory will win over this app. That is because of whitenoise's middleware behaviour - quite correct but watch out for that.
