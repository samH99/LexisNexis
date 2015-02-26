from django.conf.urls.defaults import patterns, url

from urls import urlpatterns as main_patterns

ALL_VERSIONS_RE = '(?P<version>.+)'

urlpatterns = patterns(
    '',  # base view, flake8 complains if it is on the previous line.
    url('^$',
        'djangome.views.redirect_home',
        {'version': 'latest'}),

    url('^(?P<term>[\w\-\.]+)$',
        'djangome.views.redirect_to_term',
        {'version': 'latest'}),

    url('^(?P<term>[\w\-\.]+)/stats$',
        'djangome.views.show_term',
        {'version': 'latest'}),

    url('^%s/(?P<term>[\w\-\.]+)$' % ALL_VERSIONS_RE,
        'djangome.views.redirect_to_term',
        name='redirect_to_term'),

    url('^%s/(?P<term>[\w\-\.]+)/stats$' % ALL_VERSIONS_RE,
        'djangome.views.show_term',
        name='show_term'),
)
urlpatterns += main_patterns
